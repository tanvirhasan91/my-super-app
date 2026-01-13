import streamlit as st
from gtts import gTTS
import yt_dlp
import os
import shutil

# পেজ কনফিগারেশন
st.set_page_config(page_title="My Super App", page_icon="🚀", layout="centered")

# ডাউনলোড ফোল্ডার ক্লিন করার ফাংশন
def clear_downloads():
    if os.path.exists("downloads"):
        shutil.rmtree("downloads")
    os.makedirs("downloads")

# সাইডবার
st.sidebar.title("🧰 Menu")
app_mode = st.sidebar.selectbox("Choose an App:", ["Home", "Text to Speech 🗣️", "Video Downloader 📺"])

# --- হোম পেজ ---
if app_mode == "Home":
    st.title("Welcome to My Super App 🚀")
    st.write("This application contains multiple tools.")
    st.success("👈 Please select a tool from the Sidebar menu.")
    st.image("https://cdn-icons-png.flaticon.com/512/3067/3067260.png", width=200)

# --- টেক্সট টু স্পিচ ---
elif app_mode == "Text to Speech 🗣️":
    st.header("🗣️ Text to Speech Converter")
    
    lang_options = {"English": "en", "Bengali (বাংলা)": "bn", "Hindi (हिंदी)": "hi", "Spanish": "es", "French": "fr"}
    
    col1, col2 = st.columns(2)
    with col1:
        lang_name = st.selectbox("Select Language:", list(lang_options.keys()))
        lang_code = lang_options[lang_name]
    with col2:
        speed = st.radio("Speed:", ["Normal", "Slow"])

    text = st.text_area("Enter text here:", height=150)
    
    if st.button("Convert 🎵"):
        if text:
            try:
                is_slow = True if speed == "Slow" else False
                tts = gTTS(text=text, lang=lang_code, slow=is_slow)
                tts.save("speech.mp3")
                
                audio_file = open("speech.mp3", "rb")
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3")
                st.download_button("Download Audio", audio_bytes, "speech.mp3", "audio/mp3")
                st.success(f"Done! ({lang_name})")
            except Exception as e:
                st.error(f"Error: {e}")

# --- ভিডিও ডাউনলোডার (yt-dlp দিয়ে ফিক্স করা) ---
elif app_mode == "Video Downloader 📺":
    st.header("📺 YouTube Video Downloader (Server Fixed)")
    
    url = st.text_input("Paste YouTube Link Here:")

    if st.button("Download Video ⬇️"):
        if url:
            try:
                # আগের ফাইল মুছে ফেলা
                clear_downloads()
                
                st.info("Processing... This might take a few seconds ⏳")
                
                # yt-dlp অপশন
                ydl_opts = {
                    'outtmpl': 'downloads/%(title)s.%(ext)s',
                    'format': 'best',
                    'noplaylist': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    file_path = ydl.prepare_filename(info)
                    title = info.get('title', 'Video')
                    thumbnail = info.get('thumbnail')
                
                # ফলাফল দেখানো
                if thumbnail:
                    st.image(thumbnail, width=300)
                st.success(f"✅ Ready: {title}")
                
                # ডাউনলোড বাটন
                with open(file_path, "rb") as f:
                    st.download_button(
                        label="Download to PC 📥",
                        data=f,
                        file_name=os.path.basename(file_path),
                        mime="video/mp4"
                    )
                    
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please paste a link first!")
