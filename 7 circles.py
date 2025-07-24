import streamlit as st
from moviepy.editor import ImageClip, CompositeVideoClip
from PIL import Image
import numpy as np
import os
import tempfile

st.set_page_config(page_title="Rotating Image Video Generator", layout="centered")
st.title("🎞️ Rotating Central Image Video Maker")

# --- Upload Section ---
st.markdown("### 📁 Upload Images")
central_image = st.file_uploader("Upload Central Image (1.png)", type=["png"], key="central")
rotating_images = st.file_uploader("Upload Rotating Images (2.png to 7.png)", type=["png"], accept_multiple_files=True, key="rotating")

if central_image and len(rotating_images) >= 1:
    with tempfile.TemporaryDirectory() as tmpdir:
        # Save images temporarily
        central_path = os.path.join(tmpdir, "central.png")
        with open(central_path, "wb") as f:
            f.write(central_image.read())

        rotating_paths = []
        for i, file in enumerate(rotating_images):
            img_path = os.path.join(tmpdir, f"rotate_{i}.png")
            with open(img_path, "wb") as f:
                f.write(file.read())
            rotating_paths.append(img_path)

        # --- Video Processing ---
        central_img = Image.open(central_path)
        central_size = central_img.size
        num_images = len(rotating_paths)
        radius = 300
        duration = 10
        frame_rate = 24
        num_frames = duration * frame_rate
        angle_increment = 360 / num_images

        central_clip = ImageClip(central_path).set_duration(duration)
        clips = [central_clip.set_position("center")]

        for i, img_path in enumerate(rotating_paths):
            img_clip = ImageClip(img_path).set_duration(duration)
            frames = []

            for t in range(num_frames):
                angle = (t * 360 / num_frames + i * angle_increment) % 360
                radians = np.deg2rad(angle)
                x = central_size[0] / 2 + radius * np.cos(radians) - img_clip.w / 2
                y = central_size[1] / 2 + radius * np.sin(radians) - img_clip.h / 2
                frames.append(img_clip.set_position((x, y)).get_frame(t / frame_rate))

            animated_clip = ImageClip(np.array(frames)).set_duration(duration)
            clips.append(animated_clip)

        final_clip = CompositeVideoClip(clips, size=central_size).set_duration(duration)

        st.markdown("### 🎬 Rendering Video...")
        video_output_path = os.path.join(tmpdir, "rotating_video.mp4")
        final_clip.write_videofile(video_output_path, fps=frame_rate, codec='libx264')

        with open(video_output_path, "rb") as video_file:
            st.success("✅ Video created successfully!")
            st.video(video_file)
            st.download_button("⬇️ Download Video", video_file, file_name="rotating_video.mp4", mime="video/mp4")

else:
    st.info("Upload one central image and at least one rotating image to begin.")
