# mimi.py
import streamlit as st
from openai import OpenAI
from gtts import gTTS
import tempfile

client = OpenAI(
    api_key=st.secrets["AIzaSyCf5WgWIsqxdOVCM92vUN3xXVT1L8Plfa8"]
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

st.set_page_config(
    page_title="MIMI AI",
    page_icon="🤖"
)

st.title("🤖 MIMI AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Type your message...")

if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    try:
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {
                    "role": "system",
                    "content": "You are MIMI AI. Always answer in Bengali unless the user asks for another language."
                }
            ] + st.session_state.messages
        )

        answer = response.choices[0].message.content

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("assistant"):
            st.write(answer)

            try:
                lang = "bn"

                if any(c.isalpha() for c in answer[:20]):
                    lang = "en"

                tts = gTTS(text=answer, lang=lang)

                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)

                    with open(fp.name, "rb") as audio_file:
                        audio_bytes = audio_file.read()

                st.audio(audio_bytes, format="audio/mp3")

            except Exception as voice_error:
                st.warning(f"Voice Output Error: {voice_error}")

    except Exception as e:
        st.error(f"AI Error: {e}")
