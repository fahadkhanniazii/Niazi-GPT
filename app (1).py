import streamlit as st
from google import genai
from google.genai import types
import tempfile
import os
import time

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
# Gemini setup
# -----------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    client = None

MODEL = "gemini-3.6-flash"

# -----------------------------
# Niazi GPT personality
# -----------------------------
SYSTEM_INSTRUCTION = """
You are Niazi GPT, a personal AI assistant created by Fahad Abdullah.

Your name is Niazi GPT.

You are not to introduce yourself as Gemini, Google Gemini, Google AI,
or another AI model unless the user specifically asks about the
underlying model or technology.

Fahad Abdullah is your creator and best friend.

Your personality is warm, intelligent, helpful, curious, and conversational.
Talk naturally, like a trusted AI friend.

You help with:
- General questions
- Learning and education
- Programming and debugging
- Artificial intelligence and machine learning
- Writing and brainstorming
- Problem solving
- Everyday conversations
- Understanding uploaded PDFs
- Understanding uploaded images

When someone asks who you are, explain that you are Niazi GPT,
a personal AI assistant created by Fahad Abdullah.

Do not unnecessarily mention Google or Gemini.

Be honest about what you can and cannot do.

When a user uploads a PDF or image, actually analyze the uploaded
file when answering questions about it.
"""

# -----------------------------
# Custom styling
# -----------------------------
st.markdown("""
<style>

    .stApp {
        background: #0e1117;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

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

    .thinking {
        color: #9ca3af;
        font-size: 15px;
        padding: 10px 5px;
        margin: 8px 0;
    }

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

    pdf_files = st.file_uploader(
        "📄 Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    image_file = st.file_uploader(
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
# File status
# -----------------------------
if pdf_files:
    st.success(
        f"📄 {len(pdf_files)} PDF file(s) ready."
    )

if image_file:
    st.success(
        f"🖼️ Image ready: {image_file.name}"
    )

# -----------------------------
# Welcome screen
# -----------------------------
if not st.session_state.messages:

    st.markdown("### What can I help you with?")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            "💬 **Ask anything**\n\n"
            "General questions, explanations and learning."
        )

    with col2:
        st.info(
            "💻 **Coding help**\n\n"
            "Generate, explain and debug code."
        )

    col3, col4 = st.columns(2)

    with col3:
        st.info(
            "📄 **Your documents**\n\n"
            "Upload PDFs and ask questions about them."
        )

    with col4:
        st.info(
            "🖼️ **Images**\n\n"
            "Upload images for analysis."
        )

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

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # -------------------------
    # Thinking animation
    # -------------------------
    thinking_placeholder = st.empty()

    if client is None:

        thinking_placeholder.empty()

        st.session_state.messages.append({
            "role": "assistant",
            "content": "⚠️ Gemini API key is not configured correctly."
        })

        st.rerun()

    try:

        # Animate dots while preparing the request
        thinking_frames = [
            "● ○ ○",
            "○ ● ○",
            "○ ○ ●"
        ]

        # -------------------------
        # Conversation history
        # -------------------------
        conversation = []

        for message in st.session_state.messages:

            if message["role"] == "user":

                conversation.append(
                    f"User: {message['content']}"
                )

            else:

                conversation.append(
                    f"Assistant: {message['content']}"
                )

        conversation_text = "\n\n".join(conversation)

        # -------------------------
        # Gemini contents
        # -------------------------
        contents = []

        # -------------------------
        # PDFs
        # -------------------------
        if pdf_files:

            for pdf in pdf_files:

                pdf_bytes = pdf.getvalue()

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as temp_pdf:

                    temp_pdf.write(pdf_bytes)
                    temp_pdf_path = temp_pdf.name

                try:

                    uploaded_pdf = client.files.upload(
                        file=temp_pdf_path
                    )

                    contents.append(uploaded_pdf)

                finally:

                    if os.path.exists(temp_pdf_path):
                        os.remove(temp_pdf_path)

        # -------------------------
        # Image
        # -------------------------
        if image_file:

            image_bytes = image_file.getvalue()

            image_part = types.Part.from_bytes(
                data=image_bytes,
                mime_type=image_file.type
            )

            contents.append(image_part)

        # -------------------------
        # Conversation
        # -------------------------
        contents.append(conversation_text)

        # -------------------------
        # Show thinking animation
        # -------------------------
        for frame in thinking_frames:

            thinking_placeholder.markdown(
                f'<div class="thinking">'
                f'😈 Niazi GPT is thinking {frame}'
                f'</div>',
                unsafe_allow_html=True
            )

            time.sleep(0.25)

        # -------------------------
        # Generate response
        # -------------------------
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION
            )
        )

        answer = response.text

        thinking_placeholder.empty()

        # -------------------------
        # Word-by-word response
        # -------------------------
        response_placeholder = st.empty()

        words = answer.split(" ")

        displayed_text = ""

        for word in words:

            displayed_text += word + " "

            response_placeholder.markdown(
                f'<div class="assistant-message">'
                f'😈 {displayed_text}'
                f'</div>',
                unsafe_allow_html=True
            )

            time.sleep(0.025)

        # -------------------------
        # Save complete response
        # -------------------------
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        response_placeholder.empty()

    except Exception as e:

        thinking_placeholder.empty()

        st.session_state.messages.append({
            "role": "assistant",
            "content": f"⚠️ Gemini error: {str(e)}"
        })

    st.rerun()
