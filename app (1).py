import streamlit as st

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Niazi GPT",
    page_icon="😈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom styling
# -----------------------------
st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: #0e1117;
    }

    /* Hide Streamlit branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* Main title */
    .niazi-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .niazi-subtitle {
        text-align: center;
        color: #9ca3af;
        font-size: 16px;
        margin-bottom: 35px;
    }

    /* Chat messages */
    .user-message {
        background: #1f2937;
        padding: 12px 16px;
        border-radius: 14px;
        margin: 10px 0;
    }

    .assistant-message {
        background: #151922;
        padding: 12px 16px;
        border-radius: 14px;
        margin: 10px 0;
        border: 1px solid #252b36;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #11151d;
    }

    /* Mobile adjustments */
    @media (max-width: 768px) {

        .niazi-title {
            font-size: 30px;
        }

        .niazi-subtitle {
            font-size: 14px;
            margin-bottom: 20px;
        }

        .block-container {
            padding-left: 12px;
            padding-right: 12px;
            padding-top: 15px;
        }

    }

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Session state
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.markdown("## 😈 Niazi GPT")

    st.markdown("---")

    if st.button("＋ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("### Tools")

    st.file_uploader(
        "📄 Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    st.file_uploader(
        "🖼️ Upload Image",
        type=["png", "jpg", "jpeg", "webp"]
    )

    st.markdown("---")

    st.caption("Personal AI Assistant")
    st.caption("Free-first • Built with Python")


# -----------------------------
# Main header
# -----------------------------
st.markdown(
    '<div class="niazi-title">😈 Niazi GPT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="niazi-subtitle">'
    'Your personal AI assistant'
    '</div>',
    unsafe_allow_html=True
)


# -----------------------------
# Welcome screen
# -----------------------------
if not st.session_state.messages:

    st.markdown("### What can I help you with?")

    col1, col2 = st.columns(2)

    with col1:
        st.info("💬 **Ask anything**\n\nGeneral questions, explanations and learning.")

    with col2:
        st.info("💻 **Coding help**\n\nGenerate, explain and debug code.")

    col3, col4 = st.columns(2)

    with col3:
        st.info("📄 **Your documents**\n\nUpload PDFs and ask questions about them.")

    with col4:
        st.info("🖼️ **Images**\n\nUpload images for analysis.")


# -----------------------------
# Display chat history
# -----------------------------
for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f'<div class="user-message">'
            f'🧑 {message["content"]}'
            f'</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f'<div class="assistant-message">'
            f'😈 {message["content"]}'
            f'</div>',
            unsafe_allow_html=True
        )


# -----------------------------
# Chat input
# -----------------------------
question = st.chat_input(
    "Message Niazi GPT..."
)


if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    st.rerun()