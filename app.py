import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# LOAD ENV
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY not found in .env")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

MODEL = "gpt-4o-mini"

# PAGE CONFIG
st.set_page_config(
    page_title="Bay_max",
    page_icon="Bay_max",
    layout="centered"
)

st.title("Bay_max")


# CHAT MEMORY (LIKE CHATGPT)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are ChatGPT, a helpful assistant."}
    ]

# DISPLAY CHAT
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])


# USER INPUT
user_input = st.chat_input("Send a message...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # AI response
    with st.chat_message("assistant"):
        with st.spinner("Answering as soon as possible ......."):
            response = client.chat.completions.create(
                model=MODEL,
                messages=st.session_state.messages,
                temperature=0.7
            )

            reply = response.choices[0].message.content
            st.write(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
