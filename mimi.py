import streamlit as st
from openai import OpenAI
from gtts import gTTS
import tempfile

# Page Config
st.set_page_config(
    page_title="MIMI AI",
    page_icon="🤖"
)

st.title("🤖 MIMI AI Assistant")

# Gemini Client
client = OpenAI(
    api_key=["AQ.Ab8RN6IMZjfKl-h3nZ3HIFIcNO1VCOQ-iSkvfeagAyT5TpnKjA"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input
prompt = st.chat_input("Type your message...")

if prompt:

    # Show User Message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    try:
        # Gemini Response
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=st.session_state.messages
        )

        answer = response.choices[0].message.content

        # Save AI Response
        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("assistant"):
            st.write(answer)

            # Voice Output
            try:
                tts = gTTS(text=answer, lang="bn")

                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)

                    with open(fp.name, "rb") as audio_file:
                        audio_bytes = audio_file.read()

                st.audio(audio_bytes, format="audio/mp3")

            except Exception as voice_error:
                st.warning(f"Voice Error: {voice_error}")

    except Exception as e:
        st.exception(e)
