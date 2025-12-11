import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np
import os
import tempfile
import shutil
import zipfile

def apply_effects(image, output_folder):
    effects = [
        ("grayscale", ImageOps.grayscale(image)),
        ("color_tint_red", ImageOps.colorize(ImageOps.grayscale(image), 'black', 'red')),
        ("color_tint_green", ImageOps.colorize(ImageOps.grayscale(image), 'black', 'green')),
        ("color_tint_blue", ImageOps.colorize(ImageOps.grayscale(image), 'black', 'blue')),
        ("increase_saturation", ImageEnhance.Color(image).enhance(2.0)),
        ("decrease_saturation", ImageEnhance.Color(image).enhance(0.5)),
        ("sepia", ImageOps.colorize(ImageOps.grayscale(image), '#704214', '#C0C080')),
        ("invert", ImageOps.invert(image.convert("RGB"))),
        ("increase_brightness", ImageEnhance.Brightness(image).enhance(1.5)),
        ("decrease_brightness", ImageEnhance.Brightness(image).enhance(0.5)),
        ("increase_contrast", ImageEnhance.Contrast(image).enhance(2.0)),
        ("decrease_contrast", ImageEnhance.Contrast(image).enhance(0.5)),
        ("edge_enhance", image.filter(ImageFilter.EDGE_ENHANCE)),
        ("emboss", image.filter(ImageFilter.EMBOSS)),
        ("blur", image.filter(ImageFilter.BLUR)),
        ("sharpen", image.filter(ImageFilter.SHARPEN)),
        ("detail", image.filter(ImageFilter.DETAIL)),
        ("contour", image.filter(ImageFilter.CONTOUR)),
        ("flip_left_right", image.transpose(Image.FLIP_LEFT_RIGHT)),
        ("flip_top_bottom", image.transpose(Image.FLIP_TOP_BOTTOM)),
    ]

    for name, img in effects:
        img.save(os.path.join(output_folder, f"{name}.png"))

# --- Streamlit UI ---
st.set_page_config(page_title="🖼 Image Effects Tool", layout="centered")
st.title("🖼 Apply Creative Effects to Image")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
output_name = st.text_input("Name your output ZIP file", "image_effects.zip")

if uploaded_file and st.button("✨ Apply Effects"):
    with st.spinner("Processing..."):
        with tempfile.TemporaryDirectory() as tmpdir:
            img_path = os.path.join(tmpdir, uploaded_file.name)
            with open(img_path, "wb") as f:
                f.write(uploaded_file.read())

            image = Image.open(img_path)
            apply_effects(image, tmpdir)

            zip_path = os.path.join(tmpdir, output_name)
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for filename in os.listdir(tmpdir):
                    if filename.endswith(".png"):
                        zipf.write(os.path.join(tmpdir, filename), arcname=filename)

            with open(zip_path, "rb") as zf:
                st.success("✅ All effects applied successfully!")
                st.download_button("📦 Download All Effects (ZIP)", data=zf, file_name=output_name, mime="application/zip")
