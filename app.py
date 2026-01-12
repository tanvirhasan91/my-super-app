import streamlit as st
from gtts import gTTS
from pytubefix import YouTube
import os

# ----------------- পেজ কনফিগারেশন -----------------
st.set_page_config(page_title="My Super App", page_icon="🚀", layout="centered")

# ----------------- সাইডবার (মেনু) -----------------
st.sidebar.title("🧰 Menu")
app_mode = st.sidebar.selectbox("Choose an App:", ["Home", "Text to Speech 🗣️", "Video Downloader 📺"])

# ----------------- ১. হোম পেজ (Home) -----------------
if app_mode == "Home":
    st.title("Welcome to My Super App 🚀")
    st.write("This application contains multiple tools.")
    st.success("👈 Please select a tool from the Sidebar menu.")
    st.image("https://cdn-icons-png.flaticon.com/512/3067/3067260.png", width=200)

# ----------------- ২. টেক্সট টু স্পিচ (TTS) -----------------
elif app_mode == "Text to Speech 🗣️":
    st.header("🗣️ Text to Speech Converter")
    st.write("Convert your text into audio instantly!")

    # ভাষা নির্বাচনের অপশন
    lang_options = {
        "English": "en",
        "Bengali (বাংলা)": "bn",
        "Hindi (हिंदी)": "hi",
        "Spanish": "es",
        "French": "fr"
    }

    # দুটি কলাম করা হলো (পাশাপাশি দেখানোর জন্য)
    col1, col2 = st.columns(2)

    with col1:
        # ভাষা নির্বাচন
        selected_lang_name = st.selectbox("Select Language:", list(lang_options.keys()))
        selected_lang_code = lang_options[selected_lang_name]

    with col2:
        # স্পিড নির্বাচন (Normal vs Slow)
        speed_mode = st.radio("Select Speed / গতি:", ["Normal", "Slow"])

    text_input = st.text_area("Enter text here / এখানে লিখুন:", height=150)

    if st.button("Convert to Audio 🎵"):
        if text_input:
            try:
                # স্পিড লজিক সেট করা
                # যদি Slow সিলেক্ট করে তবে slow=True, নাহলে slow=False
                is_slow = True if speed_mode == "Slow" else False

                # অডিও তৈরি
                tts = gTTS(text=text_input, lang=selected_lang_code, slow=is_slow)

                save_file = "speech.mp3"
                tts.save(save_file)

                # অডিও প্লে এবং ডাউনলোড
                audio_file = open(save_file, "rb")
                audio_bytes = audio_file.read()

                st.audio(audio_bytes, format="audio/mp3")
                st.download_button(label="Download Audio", data=audio_bytes, file_name="speech.mp3", mime="audio/mp3")

                st.success(f"Done! Language: {selected_lang_name} | Speed: {speed_mode} ✅")

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please write something first!")

# ----------------- ৩. ইউটিউব ডাউনলোডার -----------------
elif app_mode == "Video Downloader 📺":
    st.header("📺 YouTube Video Downloader")

    save_path = os.path.join(os.path.expanduser("~"), "Desktop", "MyDownloads")
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    url = st.text_input("Paste YouTube Link Here:")

    if st.button("Download Video ⬇️"):
        if url:
            try:
                st.info("Fetching video info... Please wait ⏳")
                yt = YouTube(url)

                st.image(yt.thumbnail_url, width=300)
                st.write(f"**Title:** {yt.title}")

                stream = yt.streams.get_highest_resolution()
                stream.download(save_path)

                st.success(f"✅ Video Downloaded Successfully!")
                st.write(f"📂 Saved to: `{save_path}`")

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please paste a link first!")
