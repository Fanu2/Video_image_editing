import streamlit as st
from moviepy.editor import ImageSequenceClip, AudioFileClip
import tempfile
import os
from zipfile import ZipFile
import shutil

st.title("🎬 Video Maker from Images + MP3 Audio")

uploaded_images = st.file_uploader("Upload images (PNG/JPG) or zip file with images", type=["png", "jpg", "jpeg", "zip"], accept_multiple_files=True)

uploaded_audio = st.file_uploader("Upload MP3 Audio", type=["mp3"])

output_name = st.text_input("Output video filename", value="output_video.mp4")

fps = st.number_input("Frames per second (fps)", min_value=1, max_value=60, value=24)

def save_images(files, dest_folder):
    for file in files:
        file_path = os.path.join(dest_folder, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

def extract_zip(file, dest_folder):
    with ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(dest_folder)

if st.button("Create Video"):

    if not uploaded_images:
        st.error("Please upload images or a zip containing images.")
    elif not uploaded_audio:
        st.error("Please upload an MP3 audio file.")
    elif not output_name.strip():
        st.error("Please provide a valid output filename.")
    else:
        with tempfile.TemporaryDirectory() as temp_dir:
            image_dir = os.path.join(temp_dir, "images")
            os.makedirs(image_dir, exist_ok=True)

            if len(uploaded_images) == 1 and uploaded_images[0].name.endswith(".zip"):
                with tempfile.NamedTemporaryFile(delete=False) as tmp_zip:
                    tmp_zip.write(uploaded_images[0].getbuffer())
                    tmp_zip.flush()
                    extract_zip(tmp_zip.name, image_dir)
                os.unlink(tmp_zip.name)
            else:
                save_images(uploaded_images, image_dir)

            audio_path = os.path.join(temp_dir, uploaded_audio.name)
            with open(audio_path, "wb") as f:
                f.write(uploaded_audio.getbuffer())

            image_files = sorted([os.path.join(image_dir, f) for f in os.listdir(image_dir)
                                  if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

            if not image_files:
                st.error("No images found after upload/extraction.")
            else:
                try:
                    clip = ImageSequenceClip(image_files, fps=fps)
                    audio_clip = AudioFileClip(audio_path)
                    clip = clip.set_audio(audio_clip.set_duration(clip.duration))

                    output_path = os.path.join(temp_dir, output_name)

                    clip.write_videofile(output_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)
                    st.success("✅ Video created successfully!")

                    with open(output_path, "rb") as f:
                        st.download_button("⬇️ Download Video", f, file_name=output_name, mime="video/mp4")

                except Exception as e:
                    st.error(f"Error creating video: {e}")
