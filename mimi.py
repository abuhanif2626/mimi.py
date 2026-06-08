import streamlit as st
from openai import OpenAI
from gtts import gTTS
import tempfile
import os

# ========== পেজ কনফিগার ==========
st.set_page_config(
    page_title="MIMI AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 MIMI AI Assistant")

# ========== আপনার API কী এখানে বসান ==========
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"   # <-- এখানে আপনার আসল API কী দিন

# ========== ক্লায়েন্ট তৈরি ==========
client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# ========== চ্যাট হিস্টরি ==========
if "messages" not in st.session_state:
    st.session_state.messages = []

# ========== পুরোনো মেসেজ দেখানো ==========
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ========== ইউজারের ইনপুট ==========
prompt = st.chat_input("Type your message...")

if prompt:
    # ইউজারের মেসেজ সেভ ও দেখান
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # জেমিনি থেকে রেসপন্স নেওয়া
    with st.spinner("MIMI ভাবছে..."):
        try:
            response = client.chat.completions.create(
                model="gemini-1.5-flash",   # বা gemini-2.0-flash-exp
                messages=st.session_state.messages,
                temperature=0.7
            )
            answer = response.choices[0].message.content

            # অ্যাসিস্ট্যান্টের রেসপন্স সেভ ও দেখান
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)

                # ========== ভয়েস আউটপুট (বাংলা) ==========
                try:
                    tts = gTTS(text=answer, lang="bn", slow=False)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                        tts.save(tmp.name)
                        tmp_path = tmp.name

                    with open(tmp_path, "rb") as f:
                        audio_bytes = f.read()

                    st.audio(audio_bytes, format="audio/mp3")
                    os.unlink(tmp_path)   # টেম্প ফাইল ডিলিট

                except Exception as voice_err:
                    st.warning(f"🔊 ভয়েস তৈরি করতে পারিনি: {voice_err}")

        except Exception as e:
            st.error(f"⚠️ API কল ব্যর্থ: {e}")
            st.exception(e)

# ========== সাইডবারে ক্লিয়ার বাটন ==========
with st.sidebar:
    st.markdown("### 🧹 চ্যাট ক্লিয়ার")
    if st.button("🗑️ নতুন কথোপকথন"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.caption("মডেল: gemini-1.5-flash | ভয়েস: বাংলা (gTTS)")
