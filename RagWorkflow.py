from langgraph.graph import StateGraph, END

class RagWorkflow:
    def __init__(self, document_store):
        self.document_store = document_store
        self._chain = self._build_graph()

    def _retrieve(self, state: dict) -> dict:
        state["context"] = self.document_store.search(state["question"])
        return state

    def _answer(self, state: dict) -> dict:
        context = state.get("context", [])
        state["answer"] = f"I found this: '{context[0][:100]}...'" if context else "Sorry, I don't know."
        return state

    def _build_graph(self):
        workflow = StateGraph(dict)
        workflow.add_node("retrieve", self._retrieve)
        workflow.add_node("answer", self._answer)
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "answer")
        workflow.add_edge("answer", END)
        return workflow.compile()

    def ask(self, question: str) -> dict:
        return self._chain.invoke({"question": question})

    @property
    def is_ready(self) -> bool:
        return self._chain is not None
