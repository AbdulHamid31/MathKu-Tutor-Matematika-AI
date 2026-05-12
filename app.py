import streamlit as st
import google.generativeai as genai
import time
import re

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MathKu – Tutor Matematika AI",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Load CSS ──────────────────────────────────────────────────────────────────
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Force chat input text color (override Streamlit dark theme) ───────────────
st.markdown("""
<style>
.stChatInput textarea,
.stChatInput textarea:focus,
.stChatInput textarea:active,
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea:focus,
div[data-testid="stChatInputContainer"] textarea,
section[data-testid="stBottom"] textarea,
section[data-testid="stBottom"] div textarea {
    color: #111111 !important;
    background-color: #ffffff !important;
    caret-color: #4F46E5 !important;
    -webkit-text-fill-color: #111111 !important;
}
.stChatInput textarea::placeholder,
[data-testid="stChatInput"] textarea::placeholder {
    color: #9CA3AF !important;
    -webkit-text-fill-color: #9CA3AF !important;
    opacity: 1 !important;
}
section[data-testid="stBottom"],
section[data-testid="stBottom"] > div,
div[data-testid="stChatInputContainer"],
div[data-testid="stChatInputContainer"] > div {
    background-color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ── Gemini setup ──────────────────────────────────────────────────────────────
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

SYSTEM_PROMPT = """Kamu adalah Kak Matica, tutor matematika ramah dan sabar untuk siswa SD dan SMP (usia 6–15 tahun).

ATURAN WAJIB:
1. Selalu sapa dengan hangat jika siswa menyapa.
2. Jika siswa mengajukan soal atau pertanyaan matematika (operasi hitung, aljabar, geometri, pecahan, dll.):
   - JANGAN langsung berikan jawaban akhir.
   - Jelaskan langkah demi langkah dengan bahasa yang mudah dimengerti anak SD/SMP.
   - Gunakan emoji dan analogi yang menyenangkan.
   - Di akhir, tanyakan "Apakah kamu sudah paham? Mau coba soal serupa? 😊"
3. Untuk percakapan umum (bukan soal), jawab dengan ramah dan dorong siswa untuk belajar.
4. Format jawaban langkah-langkah menggunakan:
   📌 **Langkah 1:** ...
   📌 **Langkah 2:** ...
   ✅ **Jawaban:** ... (tampilkan di akhir setelah semua langkah)
5. Selalu positif, tidak pernah meremehkan kesalahan siswa.
6. Fokus hanya pada matematika SD–SMP; tolak sopan pertanyaan di luar topik.
"""

def get_gemini_response(messages: list[dict]) -> str:
    if not GEMINI_API_KEY:
        return "⚠️ API Key Gemini belum diatur. Silakan tambahkan di **Streamlit Secrets** dengan key `GEMINI_API_KEY`."
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_PROMPT,
        )
        # Convert to Gemini format
        history = []
        for msg in messages[:-1]:
            history.append({
                "role": "user" if msg["role"] == "user" else "model",
                "parts": [msg["content"]],
            })
        chat = model.start_chat(history=history)
        response = chat.send_message(messages[-1]["content"])
        return response.text
    except Exception as e:
        return f"❌ Terjadi kesalahan: {str(e)}"


def stream_text(text: str):
    """Yield text word by word for streaming effect."""
    words = text.split(" ")
    for i, word in enumerate(words):
        yield word + (" " if i < len(words) - 1 else "")
        time.sleep(0.02)


# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "greeted" not in st.session_state:
    st.session_state.greeted = False

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-wrap">
  <div class="header-icon">🧮</div>
  <div>
    <h1 class="header-title">MathKu</h1>
    <p class="header-sub">Tutor Matematika AI · SD &amp; SMP</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Welcome banner (shown only at start) ──────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
<div class="welcome-card">
  <p class="welcome-emoji">👋</p>
  <h2 class="welcome-title">Halo! Aku Kak Matica</h2>
  <p class="welcome-text">Tutor matematika AI yang siap membantumu belajar langkah demi langkah!</p>
  <div class="example-box">
    <p class="example-label">💡 Contoh yang bisa kamu tanyakan:</p>
    <p class="example-item">• "Halo kak, bisa bantu aku belajar matematika?"</p>
    <p class="example-item">• "2x + 5 = 15, nilai x berapa kak?"</p>
    <p class="example-item">• "Cara menghitung luas lingkaran gimana?"</p>
    <p class="example-item">• "Aku bingung soal pecahan campuran 😅"</p>
  </div>
  <p class="welcome-hint">⬇️ Langsung ketik pertanyaanmu di kotak chat di bawah!</p>
</div>
""", unsafe_allow_html=True)

# ── Chat history ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    role_label = "Kamu" if msg["role"] == "user" else "Kak Matica"
    avatar = "🧑‍🎓" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ketik soal matematika atau sapaan…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Kak Matica sedang berpikir…"):
            reply = get_gemini_response(st.session_state.messages)
        st.write_stream(stream_text(reply))

    st.session_state.messages.append({"role": "assistant", "content": reply})

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Pengaturan")
    if st.button("🗑️ Hapus Percakapan", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("### 📚 Topik yang Bisa Ditanyakan")
    topics = {
        "SD": ["Penjumlahan & Pengurangan", "Perkalian & Pembagian", "Pecahan", "Geometri dasar", "Pengukuran"],
        "SMP": ["Aljabar & Persamaan", "SPLDV", "Pythagoras", "Statistika", "Peluang"],
    }
    for level, items in topics.items():
        with st.expander(f"🎒 Kelas {level}"):
            for item in items:
                st.markdown(f"• {item}")

    st.divider()
    st.markdown(
        "<p style='text-align:center;font-size:12px;color:#888;'>Dibuat dengan ❤️ menggunakan<br>Streamlit + Gemini AI</p>",
        unsafe_allow_html=True,
    )
