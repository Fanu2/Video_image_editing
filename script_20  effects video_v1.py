from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np
import os


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

    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Apply and save effects
    for name, img in effects:
        img.save(os.path.join(output_folder, f"{name}.png"))


# Define the input image path and output folder
input_image_path = "/home/jasvir/Music/Data4/ut.jpg"  # Update with your image path
output_folder = "/home/jasvir/Music/Jacinta2"

# Open the input image
image = Image.open(input_image_path)

# Apply effects and save images
apply_effects(image, output_folder)
