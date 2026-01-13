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
                
                with open("speech.mp3", "rb") as audio_file:
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format="audio/mp3")
                    st.download_button("Download Audio", audio_bytes, "speech.mp3", "audio/mp3")
                    st.success(f"Done! ({lang_name})")
            except Exception as e:
                st.error(f"Error: {e}")

# --- ভিডিও ডাউনলোডার (টাইটেল ফিক্সড) ---
elif app_mode == "Video Downloader 📺":
    st.header("📺 YouTube Video Downloader (Server Fixed)")
    
    url = st.text_input("Paste YouTube Link Here:")

    if st.button("Download Video ⬇️"):
        if url:
            try:
                clear_downloads()
                st.info("Processing... This might take a few seconds ⏳")
                
                # টাইটেল সমস্যা এড়াতে ফিক্সড নাম ব্যবহার করা হচ্ছে
                ydl_opts = {
                    'outtmpl': 'downloads/my_video.%(ext)s', 
                    'format': 'best',
                    'noplaylist': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    video_title = info.get('title', 'Video')
                    
                    # ফাইল খুঁজে বের করা (mp4 বা mkv হতে পারে)
                    downloaded_file = None
                    for file in os.listdir("downloads"):
                        if file.startswith("my_video"):
                            downloaded_file = os.path.join("downloads", file)
                            break
                    
                    if downloaded_file:
                        st.success(f"✅ Ready: {video_title}")
                        with open(downloaded_file, "rb") as f:
                            st.download_button(
                                label="Download to PC 📥",
                                data=f,
                                file_name=f"{video_title}.mp4", # ডাউনলোডের সময় আসল নাম দেখাবে
                                mime="video/mp4"
                            )
                    else:
                        st.error("Error: File not found after download.")
                    
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please paste a link first!")
