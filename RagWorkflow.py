import json
import logging
import re
from google import genai
from google.genai import types
from langgraph.graph import StateGraph, END
from prompts import FACT_CHECK_PROMPT, ANSWER_PROMPTS

logger = logging.getLogger(__name__)


class RagWorkflow:
    VALID_MODES = frozenset(ANSWER_PROMPTS.keys()) | {"fact_check"}

    def __init__(self, document_store, api_key: str):
        self.document_store = document_store
        self.client = genai.Client(api_key=api_key)
        self._chain = self._build_graph()

    @staticmethod
    def _sanitize(text: str) -> str:
        """Strip null bytes and normalize whitespace to reduce prompt injection surface."""
        text = text.replace("\x00", "")
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def _retrieve(self, state: dict) -> dict:
        state["context"] = self.document_store.search(state["question"])
        return state

    def _answer(self, state: dict) -> dict:
        context = state.get("context", [])
        mode = state.get("mode", "ringkas")

        if mode not in self.VALID_MODES:
            logger.warning("Mode tidak valid '%s', fallback ke 'ringkas'", mode)
            mode = "ringkas"

        if not context:
            state["answer"] = "Maaf, tidak ditemukan informasi yang relevan dalam knowledge base."
            return state

        context_text = "\n\n".join(context)
        question = self._sanitize(state["question"])

        try:
            if mode == "fact_check":
                prompt = FACT_CHECK_PROMPT.format(question=question, context=context_text)
                res = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(response_mime_type="application/json"),
                )
                try:
                    state["answer"] = json.loads(res.text)
                except json.JSONDecodeError:
                    logger.error("Gemini mengembalikan JSON tidak valid untuk fact-check")
                    state["answer"] = {
                        "status": "ERROR",
                        "summary": "Gagal memproses respons model.",
                        "explanation": "",
                        "sources": [],
                    }
            else:
                prompt = ANSWER_PROMPTS[mode].format(question=question, context=context_text)
                res = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )
                state["answer"] = res.text or "Model tidak menghasilkan jawaban."

        except Exception as e:
            logger.error("Gemini API error pada mode '%s': %s", mode, e, exc_info=True)
            err_str = str(e).upper()
            status = getattr(e, "status_code", 0) or getattr(e, "code", 0)
            is_transient = (
                status in (429, 503)
                or "RESOURCE_EXHAUSTED" in err_str
                or "QUOTA_EXHAUSTED" in err_str
                or "UNAVAILABLE" in err_str
            )
            if is_transient:
                logger.warning("Kuota Gemini habis — fallback ke raw retrieval")
                state["llm_fallback"] = True
                if mode == "fact_check":
                    state["answer"] = {
                        "status": "PERLU BUKTI LEBIH LANJUT",
                        "summary": "Model AI tidak tersedia (kuota habis). Berikut kutipan langsung dari knowledge base.",
                        "explanation": "\n\n---\n\n".join(context),
                        "sources": [],
                    }
                else:
                    state["answer"] = "\n\n---\n\n".join(context)
                return state
            raise RuntimeError("QUOTA_EXHAUSTED") from e

        return state

    def _build_graph(self):
        workflow = StateGraph(dict)
        workflow.add_node("retrieve", self._retrieve)
        workflow.add_node("answer", self._answer)
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "answer")
        workflow.add_edge("answer", END)
        return workflow.compile()

    def ask(self, question: str, mode: str = "ringkas") -> dict:
        return self._chain.invoke({"question": question, "mode": mode})

    def fact_check(self, question: str) -> dict:
        return self._chain.invoke({"question": question, "mode": "fact_check"})

    @property
    def is_ready(self) -> bool:
        return self._chain is not None
