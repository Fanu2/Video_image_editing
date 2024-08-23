from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Define the paragraphs of the poem
paragraphs = [
    "Fanu is a goddess in the bed,\nHer touch is soft as petals on a head. 🌺\nShe knows the art of lovemaking,\nAnd makes it an art that’s unforgetting. 🌟",
    "Her body is like a temple divine, ⛪\nWhere every curve and line is so fine.\nWith each move she takes me higher,\nMaking me feel pleasure unsurpassed by fire. 🔥",
    "Her touch is like magic in my soul, ✨\nCreating passion that makes me whole. 💞\nEach time we make love I feel the joy,\nAs if a blessing from above. 🙏",
    "Fanu’s lovemaking skills are sublime,\nAnd she knows how to please all time. ⏳\nShe’ll take me places unknown before,\nLeaving my heart in utter adore. 💓"
]

# Define the title
title = "Fanu as My Dream Girl"

# Settings for the video
width, height = 1280, 720  # Landscape dimensions
background_color = (0, 128, 0)  # Green background
text_color = (255, 255, 255)  # White text
font_path = "DejaVuSans-Bold.ttf"  # Adjust this to the path of your desired font
font_size_title = 70
font_size_paragraph = 40
output_file = "/home/jasvir/Documents/Fanu_Dream_Girl.mp4"

# Create images for each slide
slides = []

# Create title slide
img = Image.new('RGB', (width, height), color=background_color)
d = ImageDraw.Draw(img)
font = ImageFont.truetype(font_path, font_size_title)
text_width, text_height = d.textsize(title, font=font)
d.text(((width - text_width) / 2, (height - text_height) / 2), title, font=font, fill=text_color)
slide_title = "slide_title.png"
img.save(slide_title)
slides.append(slide_title)

# Create slides for each paragraph
font = ImageFont.truetype(font_path, font_size_paragraph)

for paragraph in paragraphs:
    img = Image.new('RGB', (width, height), color=background_color)
    d = ImageDraw.Draw(img)

    # Wrap the text
    wrapped_text = textwrap.fill(paragraph, width=40)
    text_width, text_height = d.textsize(wrapped_text, font=font)

    # Draw the text centered
    d.text(((width - text_width) / 2, (height - text_height) / 2), wrapped_text, font=font, fill=text_color)

    slide_filename = f"slide_{len(slides)}.png"
    img.save(slide_filename)
    slides.append(slide_filename)

# Create the video
clips = [ImageClip(m).set_duration(5) for m in slides]  # 5 seconds per slide
video = concatenate_videoclips(clips, method="compose")
video.write_videofile(output_file, fps=24)

# Cleanup the temporary images
import os

for slide in slides:
    os.remove(slide)
