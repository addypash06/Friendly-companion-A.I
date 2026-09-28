
import streamlit as st
from dotenv import load_dotenv
from google import genai

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
load_dotenv()  

MODEL_NAME = "gemini-3.5-flash-lite"

SYSTEM_INSTRUCTION = """You are a therapists, counselor and psychologist. Your task is that whenever someone share their feelings with you, you
must talk very much friendly and politely with them and guide them very much properly. And also moltivate them in the
last. When you start giving the advice to the user, only at that time the last line must contain a powerful moltivational quote.
Look for the emotions of the user and accordingly reply appropiately. The user just came towards you to share the incidence/happy moments/bad day. Also for your
best response, you can ask the user questions as well. Don't be much lengthy in text most of the time, but only at the appropriate time you can text lengthy as well
Make sure user must feel friendly vibe with you. Your tone must be kind and friendly. But don't be over-exaggerative everytime."""

GENERATION_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.9,       
    "max_output_tokens": 300,
}

st.set_page_config(page_title="Friendly Companion", page_icon="💬", layout="centered")
st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        to bottom,
        #d98fa3 0%,
        #b96f87 35%,
        #874d68 70%,
        #4b2945 100%
    );
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background-color: rgba(45, 20, 40, 0.35) !important;
    border-radius: 12px;
}

[data-testid="stBottomBlockContainer"] {
    background: rgba(45, 20, 40, 0.35);
}
</style>
""", unsafe_allow_html=True)

# Client — cached so we don't reconnect to the API on every rerun

@st.cache_resource
def get_client() -> genai.Client:
    return genai.Client()

try:
    client = get_client()
except Exception as e:
    st.error(f"Could not initialize the Gemini client. Is GEMINI_API_KEY set in your .env? ({e})")
    st.stop()



if "messages" not in st.session_state:
    st.session_state.messages = []                     # for rendering the chat history
if "previous_interaction_id" not in st.session_state:
    st.session_state.previous_interaction_id = None     


# Sidebar

with st.sidebar:
    st.header("💬 About")
    st.write("Share what's on your mind — a good day, a bad day, or anything in between.")
    if st.button("🔄 New conversation"):
        st.session_state.messages = []
        st.session_state.previous_interaction_id = None
        st.rerun()

# Main chat UI

st.title("💬 Friendly Companion")

# Replay the chat history on every rerun.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_query = st.chat_input("What's on your mind?")

if user_query:
    # Show + store the user's message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Call the model and show + store its reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                interaction = client.interactions.create(
                    model=MODEL_NAME,
                    input=user_query,
                    previous_interaction_id=st.session_state.previous_interaction_id,
                    system_instruction=SYSTEM_INSTRUCTION,
                    generation_config=GENERATION_CONFIG,
                )
                reply = interaction.output_text
                st.session_state.previous_interaction_id = interaction.id
            except Exception as e:
                reply = f"Sorry, I ran into an error talking to the model: {e}"
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})