import streamlit as st
from PIL import Image
from gemini_bot import get_gemini_response, MODEL_NAME

st.set_page_config(
    page_title="Gemini Multimodal Chatbot",
    page_icon="🤖",
    layout="wide",
)

# ---------- Color theme: yellow and dark brown ----------
BG_MAIN = "#2A1E16"
BG_SIDEBAR = "#1A120C"
BG_CARD = "#3A2A1E"
BORDER = "#5A4330"
ACCENT = "#FFC93C"
ACCENT_HOVER = "#E8A317"
TEXT = "#FFF3D1"
TEXT_MUTED = "#C9B89A"

THEME_CSS = f"""
<style>
/* ----- Page background ----- */
.stApp {{
    background: linear-gradient(180deg, {BG_MAIN} 0%, #1E150F 100%);
    color: {TEXT};
}}
[data-testid="stHeader"] {{
    background: transparent;
}}

/* ----- Sidebar ----- */
[data-testid="stSidebar"] {{
    background: {BG_SIDEBAR};
    border-right: 1px solid {BORDER};
}}
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {{
    color: {ACCENT} !important;
}}

/* ----- Text and headings ----- */
h1, h2, h3 {{
    color: {ACCENT} !important;
}}
p, li, label, span {{
    color: {TEXT};
}}
[data-testid="stCaptionContainer"] p {{
    color: {TEXT_MUTED} !important;
}}
hr {{
    border-color: {BORDER} !important;
}}

/* ----- Hero banner ----- */
.hero {{
    background: linear-gradient(135deg, {BG_CARD} 0%, {BG_MAIN} 100%);
    border: 1px solid {BORDER};
    border-left: 6px solid {ACCENT};
    border-radius: 18px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
}}
.hero-title {{
    font-size: 2rem;
    font-weight: 800;
    color: {ACCENT};
    margin-bottom: 0.3rem;
}}
.hero-sub {{
    color: #E9D9B5;
    font-size: 1rem;
}}
.badge {{
    display: inline-block;
    background: {ACCENT};
    color: {BG_MAIN};
    font-weight: 700;
    font-size: 0.8rem;
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    margin-top: 0.7rem;
    margin-right: 0.4rem;
}}

/* ----- Welcome card ----- */
.welcome-card {{
    background: {BG_CARD};
    border: 1px dashed {ACCENT};
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    color: {TEXT};
    margin-bottom: 1rem;
}}
.welcome-card strong {{
    color: {ACCENT};
}}

/* ----- Buttons ----- */
.stButton > button {{
    width: 100%;
    background: {ACCENT};
    color: {BG_MAIN};
    border: none;
    border-radius: 10px;
    font-weight: 700;
    padding: 0.6rem 1rem;
    transition: all 0.2s ease;
}}
.stButton > button:hover {{
    background: {ACCENT_HOVER};
    color: {BG_SIDEBAR};
    transform: translateY(-1px);
}}
.stButton > button:focus:not(:active) {{
    border-color: {TEXT};
    color: {BG_MAIN};
}}

/* ----- Chat messages ----- */
[data-testid="stChatMessage"] {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-left: 4px solid {ACCENT};
    border-radius: 14px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.8rem;
}}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {{
    color: {TEXT} !important;
}}
[data-testid="stChatMessage"] code {{
    background: {BG_MAIN};
    color: {ACCENT};
}}
[data-testid="stChatMessage"] img {{
    border-radius: 12px;
    border: 2px solid {BORDER};
}}

/* ----- Bottom chat input bar ----- */
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"] {{
    background: {BG_MAIN} !important;
}}
[data-testid="stChatInput"] {{
    background: {BG_CARD} !important;
    border: 2px solid {ACCENT} !important;
    border-radius: 14px !important;
}}
[data-testid="stChatInput"] textarea {{
    color: {TEXT} !important;
    background: transparent !important;
}}
[data-testid="stChatInput"] textarea::placeholder {{
    color: {TEXT_MUTED} !important;
}}
[data-testid="stChatInputSubmitButton"] {{
    color: {ACCENT} !important;
}}

/* ----- File uploader ----- */
[data-testid="stFileUploader"] section {{
    background: {BG_CARD};
    border: 2px dashed {ACCENT};
    border-radius: 14px;
}}
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] p {{
    color: {TEXT} !important;
}}
[data-testid="stFileUploader"] button {{
    background: {ACCENT} !important;
    color: {BG_MAIN} !important;
    border: none !important;
    font-weight: 700;
}}

/* ----- Info, spinner ----- */
[data-testid="stAlert"] {{
    background: {BG_CARD};
    border: 1px solid {ACCENT};
    border-radius: 12px;
}}
[data-testid="stAlert"] p {{
    color: {TEXT} !important;
}}
[data-testid="stSpinner"] p {{
    color: {ACCENT} !important;
}}
</style>
"""

st.markdown(THEME_CSS, unsafe_allow_html=True)

# ---------- Session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🍯 Chat controls")

    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown(f"**Model:** `{MODEL_NAME}`")
    st.markdown("**Modes:** Text + Image")
    st.info("Your API key is read from the project's .env file. Never share it.")

# ---------- Header ----------
st.markdown(
    f"""
    <div class="hero">
        <div class="hero-title">🤖 Gemini Multimodal Chatbot</div>
        <div class="hero-sub">Ask questions using text, or upload an image and ask Gemini about it.</div>
        <span class="badge">{MODEL_NAME}</span>
        <span class="badge">Text + Image</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Welcome card when chat is empty ----------
if not st.session_state.messages:
    st.markdown(
        """
        <div class="welcome-card">
            <strong>Welcome!</strong> Type a question below to start.
            You can also upload a PNG, JPG, JPEG, or WEBP image and ask
            Gemini to explain it.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- Previous messages ----------
for message in st.session_state.messages:
    avatar = "🧑" if message["role"] == "user" else "✨"
    with st.chat_message(message["role"], avatar=avatar):
        if message.get("image") is not None:
            st.image(message["image"], caption="Uploaded image", width=320)
        st.markdown(message["content"])

# ---------- Optional image upload ----------
uploaded_file = st.file_uploader(
    "🖼️ Optional: upload an image",
    type=["png", "jpg", "jpeg", "webp"],
    help="Upload an image, then type a question below.",
)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Image ready for Gemini", width=360)
else:
    image = None

# ---------- Chat input and response ----------
prompt = st.chat_input("Type your message or ask a question about the image...")

if prompt:
    user_message = {"role": "user", "content": prompt, "image": image}
    st.session_state.messages.append(user_message)

    with st.chat_message("user", avatar="🧑"):
        if image is not None:
            st.image(image, width=320)
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="✨"):
        with st.spinner("Gemini is thinking..."):
            try:
                history = [
                    {"role": item["role"], "content": item["content"]}
                    for item in st.session_state.messages[:-1]
                ]
                answer = get_gemini_response(prompt, image, history)
                st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer, "image": None}
                )
            except Exception as error:
                st.error(f"Something went wrong: {error}")