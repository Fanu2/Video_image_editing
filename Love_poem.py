import streamlit as st
from moviepy.editor import ImageClip, concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

st.set_page_config(page_title="🎬 Poem Video Maker", layout="centered")
st.title("🎥 Poem to Video Generator")

# --- Settings ---
width, height = 1280, 720
background_color = (0, 128, 0)
text_color = (255, 255, 255)
font_size_title = 70
font_size_paragraph = 40
font_path = "DejaVuSans-Bold.ttf"  # Ensure this font file exists

# --- Sample poem data ---
title = "Fanu as My Dream Girl"
paragraphs = [
    "Fanu is a goddess in the bed,\nHer touch is soft as petals on a head. 🌺\nShe knows the art of lovemaking,\nAnd makes it an art that’s unforgetting. 🌟",
    "Her body is like a temple divine, ⛪\nWhere every curve and line is so fine.\nWith each move she takes me higher,\nMaking me feel pleasure unsurpassed by fire. 🔥",
    "Her touch is like magic in my soul, ✨\nCreating passion that makes me whole. 💞\nEach time we make love I feel the joy,\nAs if a blessing from above. 🙏",
    "Fanu’s lovemaking skills are sublime,\nAnd she knows how to please all time. ⏳\nShe’ll take me places unknown before,\nLeaving my heart in utter adore. 💓"
]

if st.button("✨ Generate Video"):
    slides = []

    # Title slide
    img = Image.new('RGB', (width, height), color=background_color)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, font_size_title)
    w, h = draw.textsize(title, font=font)
    draw.text(((width - w) / 2, (height - h) / 2), title, font=font, fill=text_color)
    img.save("slide_title.png")
    slides.append("slide_title.png")

    # Paragraph slides
    font = ImageFont.truetype(font_path, font_size_paragraph)
    for idx, paragraph in enumerate(paragraphs):
        img = Image.new('RGB', (width, height), color=background_color)
        draw = ImageDraw.Draw(img)
        wrapped = textwrap.fill(paragraph, width=40)
        w, h = draw.textsize(wrapped, font=font)
        draw.text(((width - w) / 2, (height - h) / 2), wrapped, font=font, fill=text_color)
        fname = f"slide_{idx+1}.png"
        img.save(fname)
        slides.append(fname)

    # Generate video
    clips = [ImageClip(slide).set_duration(5) for slide in slides]
    final_clip = concatenate_videoclips(clips, method="compose")
    output_path = "fanu_poem_video.mp4"
    final_clip.write_videofile(output_path, fps=24)

    # Show in Streamlit
    st.video(output_path)

    # Download link
    with open(output_path, "rb") as f:
        st.download_button("⬇️ Download Video", f, file_name="fanu_poem_video.mp4", mime="video/mp4")

    # Cleanup
    for slide in slides:
        os.remove(slide)
    os.remove(output_path)
