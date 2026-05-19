import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")
MAX_INPUT_CHARS = 2000

st.set_page_config(page_title="HealthTruth-AI", page_icon="🩺 💊", layout="centered")

st.markdown("""
<style>
    div[data-testid="stChatMessage"] { padding: 0.5rem 0; }
    .profile-card {
        background: #f0f7ff;
        border-left: 3px solid #4a90d9;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 0.85em;
        margin-top: 6px;
        line-height: 1.7;
    }
    .block-container { padding-bottom: 5rem !important; }
</style>
""", unsafe_allow_html=True)

if "profile" not in st.session_state:
    st.session_state.profile = {"name": "", "gender": "", "age": 0,
                                 "conditions": [], "allergies": [], "medications": []}
if "messages" not in st.session_state:
    st.session_state.messages = []


def profile_is_active(p):
    return any([p.get("gender"), p.get("age"), p.get("conditions"),
                p.get("allergies"), p.get("medications")])


def build_profile_context(profile):
    parts = []
    demo = [x for x in [profile.get("gender"), f"{profile['age']} tahun" if profile.get("age") else ""] if x]
    if demo:
        parts.append("Demografi: " + ", ".join(demo))
    if profile.get("conditions"):
        parts.append("Kondisi kesehatan: " + ", ".join(profile["conditions"]))
    if profile.get("allergies"):
        parts.append("Alergi: " + ", ".join(profile["allergies"]))
    if profile.get("medications"):
        parts.append("Obat rutin: " + ", ".join(profile["medications"]))
    if not parts:
        return ""
    return "[Profil pengguna: " + " | ".join(parts) + "]\n\n"


def call_api(user_input, is_fact_check, answer_mode, profile):
    profile_ctx = build_profile_context(profile)
    enriched = profile_ctx + user_input
    is_personalized = bool(profile_ctx)

    if is_fact_check:
        resp = requests.post(f"{API_URL}/fact-check", json={"claim": enriched}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        result = data.get("result", {})
        verdict = result.get("status", "")
        color = {"FAKTA": "green", "MITOS": "red"}.get(verdict, "orange")
        answer_text = (
            f"**:{color}[{verdict}]**\n\n"
            f"{result.get('summary', '')}\n\n"
            f"{result.get('explanation', '')}"
        )
        return answer_text, {
            "verdict": verdict,
            "sources": result.get("sources", []),
            "context": data.get("context_used", []),
            "latency": data.get("latency_sec", 0),
            "personalized": is_personalized,
            "llm_fallback": data.get("llm_fallback", False),
        }

    resp = requests.post(f"{API_URL}/ask",
                         json={"question": enriched, "mode": answer_mode}, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data.get("answer", ""), {
        "context": data.get("context_used", []),
        "latency": data.get("latency_sec", 0),
        "personalized": is_personalized,
        "llm_fallback": data.get("llm_fallback", False),
    }


with st.sidebar:
    st.markdown("## 🩺 💊 HealthTruth-AI")
    st.caption("Pengecekan mitos obat tradisional berbasis bukti ilmiah")

    st.divider()

    st.caption("MODE")
    mode_label = st.segmented_control(
        "mode", options=["💬 Tanya", "🔍 Cek Fakta"], default="💬 Tanya",
        label_visibility="collapsed",
    ) or "💬 Tanya"
    is_fact_check = mode_label == "🔍 Cek Fakta"

    if not is_fact_check:
        st.caption("KEDALAMAN JAWABAN")
        depth_label = st.segmented_control(
            "depth", options=["Ringkas", "Detail", "Sumber"], default="Ringkas",
            label_visibility="collapsed",
            help="**Ringkas** — 2-3 kalimat  \n**Detail** — lengkap berbasis bukti  \n**Sumber** — disertai rujukan resmi",
        ) or "Ringkas"
        answer_mode = depth_label.lower()
    else:
        answer_mode = "ringkas"

    st.divider()

    p = st.session_state.profile
    active = profile_is_active(p)

    expander_title = (
        f"👤 {p['name']} — Edit Profil" if p.get("name")
        else "👤 Edit Profil" if active
        else "👤 Profil Kesehatan"
    )

    if active:
        lines = []
        demo = [x for x in [p.get("gender"), f"{p.get('age')} th" if p.get("age") else ""] if x]
        if demo:
            lines.append("🧑 " + ", ".join(demo))
        lines += [f"🩺 {c}" for c in p.get("conditions", [])]
        lines += [f"⚠️ Alergi {a}" for a in p.get("allergies", [])]
        lines += [f"💊 {m}" for m in p.get("medications", [])]
        st.markdown('<div class="profile-card">' + "<br>".join(lines) + "</div>",
                    unsafe_allow_html=True)
        st.write("")

    with st.expander(expander_title, expanded=not active):
        if not active:
            st.info("Isi profil agar jawabanku lebih relevan untuk kondisi kesehatanmu.", icon="💡")
            st.write("")

        name = st.text_input("Nama (opsional)", value=p.get("name", ""), placeholder="mis. Budi")
        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox("Jenis kelamin", ["", "Pria", "Wanita"],
                                  index=["", "Pria", "Wanita"].index(p.get("gender", "")))
        with col2:
            age = st.number_input("Usia", min_value=0, max_value=120, value=int(p.get("age", 0)))

        conditions = st.multiselect(
            "Kondisi kesehatan",
            ["Diabetes Tipe 2", "Hipertensi", "Obesitas", "Gagal Ginjal",
             "Hamil/Menyusui", "Asam Urat", "Kolesterol Tinggi", "Gangguan Hati", "Asma"],
            default=p.get("conditions", []), placeholder="Pilih kondisi yang relevan…")
        allergies = st.multiselect(
            "Alergi",
            ["Jahe", "Kunyit", "Kayu Manis", "Aspirin/NSAID",
             "Kacang", "Seafood", "Lateks", "Propolis/Madu"],
            default=p.get("allergies", []), placeholder="Pilih alergi yang kamu miliki…")
        medications = st.multiselect(
            "Obat yang rutin dikonsumsi",
            ["Warfarin/Pengencer darah", "Metformin", "Insulin", "Amlodipin",
             "Simvastatin/Statin", "Antidepresan", "Obat tiroid", "Aspirin dosis rendah"],
            default=p.get("medications", []), placeholder="Pilih obat rutin…")

        if st.button("💾 Simpan Profil", use_container_width=True, type="primary"):
            st.session_state.profile = {
                "name": name, "gender": gender, "age": age,
                "conditions": conditions, "allergies": allergies, "medications": medications,
            }
            st.rerun()

        if active and st.button("Hapus profil", use_container_width=True):
            st.session_state.profile = {
                "name": "", "gender": "", "age": 0,
                "conditions": [], "allergies": [], "medications": []}
            st.rerun()

    st.divider()

    if st.button("📡 Cek Status API", use_container_width=True):
        try:
            r = requests.get(f"{API_URL}/status", timeout=5)
            d = r.json()
            if d.get("graph_ready") and d.get("qdrant_ready"):
                st.success("API aktif · Qdrant terhubung ✓")
            elif d.get("graph_ready"):
                st.warning("API aktif · Qdrant offline (in-memory)")
            else:
                st.error("API belum siap")
        except Exception:
            st.error("Tidak dapat terhubung ke API")

    if st.button("🗑 Hapus Riwayat Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


if st.session_state.get("pending_input"):
    incoming = st.session_state.pop("pending_input")
    if incoming and len(incoming) <= MAX_INPUT_CHARS:
        st.session_state.messages.append({"role": "user", "content": incoming})
        st.session_state["_process_q"] = incoming

greeting = f"Halo, {p['name']}! 👋" if p.get("name") else "Halo! 👋"

if st.session_state.get("_process_q"):
    question = st.session_state.pop("_process_q")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    with st.chat_message("assistant"):
        with st.spinner("Sedang mencari jawaban…"):
            try:
                answer_text, meta = call_api(
                    question, is_fact_check, answer_mode, st.session_state.profile
                )
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer_text, "meta": meta}
                )
            except requests.exceptions.ConnectionError:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Tidak bisa terhubung ke API. Jalankan dulu: `docker compose up -d`"
                })
            except requests.exceptions.HTTPError as e:
                st.session_state.messages.append({"role": "assistant", "content": (
                    "⏳ Kuota API harian habis. Coba lagi besok atau aktifkan billing di "
                    "[Google AI Studio](https://aistudio.google.com)."
                    if e.response.status_code == 429
                    else f"Server error ({e.response.status_code}). Coba beberapa saat lagi."
                )})
            except Exception:
                st.session_state.messages.append(
                    {"role": "assistant", "content": "Terjadi kesalahan. Coba lagi."}
                )
    st.rerun()

elif not st.session_state.messages:
    welcome = st.empty()
    with welcome.container():
        st.markdown(f"## {greeting}")
        st.markdown(
            "Saya **HealthTruth-AI** — asisten pengecekan informasi obat tradisional berbasis bukti ilmiah."
            if not active
            else "Saya **HealthTruth-AI**. Profil kesehatanmu sudah tersimpan — jawaban akan disesuaikan."
        )
        if not active:
            st.info("**Tips:** Isi profil kesehatan di sidebar agar jawabanku lebih relevan untukmu.", icon="💡")
        st.markdown("#### Coba tanyakan:")
        suggestions = (
            ["Daun sirsak bisa menyembuhkan kanker",
             "Madu aman untuk penderita diabetes",
             "Bawang putih seefektif statin untuk kolesterol",
             "Propolis bisa membunuh semua virus dan bakteri"]
            if is_fact_check else
            ["Apakah kunyit bisa menggantikan obat anti-inflamasi?",
             "Apa risiko minum jamu setiap hari?",
             "Bolehkah penderita hipertensi minum jamu?",
             "Apa perbedaan jamu, OHT, dan fitofarmaka?"]
        )
        col1, col2 = st.columns(2)
        for i, q in enumerate(suggestions):
            with (col1 if i % 2 == 0 else col2):
                if st.button(q, use_container_width=True, key=f"sug_{i}"):
                    welcome.empty()
                    st.session_state.pending_input = q
                    st.rerun()

else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "meta" not in msg:
                continue
            meta = msg["meta"]
            if meta.get("llm_fallback"):
                st.warning("⚠️ Model AI tidak tersedia (kuota habis) — kutipan langsung dari knowledge base.", icon="⚠️")
            elif meta.get("personalized"):
                st.caption("✨ Disesuaikan dengan profil kesehatanmu")
            with st.expander("Lihat detail & sumber", expanded=False):
                if meta.get("verdict"):
                    color = {"FAKTA": "green", "MITOS": "red"}.get(meta["verdict"], "orange")
                    st.markdown(f"**Verdict:** :{color}[{meta['verdict']}]")
                if meta.get("sources"):
                    st.markdown("**Sumber:** " + ", ".join(meta["sources"]))
                if meta.get("context"):
                    st.markdown("**Dokumen referensi yang digunakan:**")
                    for i, ctx in enumerate(meta["context"], 1):
                        st.caption(f"{i}. {ctx[:220]}…" if len(ctx) > 220 else f"{i}. {ctx}")
                if meta.get("latency"):
                    st.caption(f"⏱ Waktu respons: {meta['latency']:.2f} detik")


placeholder = (
    "Tulis klaim yang ingin dicek, mis: 'Daun sirsak menyembuhkan kanker'…"
    if is_fact_check
    else "Tulis pertanyaanmu tentang obat tradisional…"
)
user_input = st.chat_input(placeholder)
if user_input:
    if len(user_input) > MAX_INPUT_CHARS:
        st.warning(f"Pertanyaan terlalu panjang. Maksimal {MAX_INPUT_CHARS} karakter.")
        st.stop()
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state["_process_q"] = user_input
    st.rerun()
