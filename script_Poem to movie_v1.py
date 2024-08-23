from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# Poem text
title = "Lady of Roses"
poem_paragraphs = [
    "In the highlands where the green hills sway,\nLives a woman who brightens the day.\nMs. Jacinta, with a heart so pure,\nHer passion and kindness ever endure.",
    "Nature's lover, with a gentle hand,\nShe nurtures the green of this beautiful land.\nHer garden blooms with roses so fine,\nA testament to her love, a fragrant sign.",
    "Awarded for excellence, her dedication clear,\nShe guides with wisdom, wipes away fear.\nA national treasure, her students adore,\nA beacon of knowledge, opening each door.",
    "In the school she leads with grace,\nEvery child finds a welcoming place.\nHer sympathy and care, like a gentle breeze,\nTouch the lives of many, putting hearts at ease.",
    "Green is her color, a symbol of life,\nIn protecting the earth, she faces no strife.\nHer rose garden blooms, a sight to behold,\nA story of love in petals untold.",
    "Lady of Roses, with a heart so kind,\nIn you, a true friend and guardian we find.\nYour legacy grows with every rose,\nIn the Highland's heart, your love forever glows."
]

# Font settings
title_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
paragraph_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
title_font_size = 48
paragraph_font_size = 32

# Image settings
image_width = 800
image_height = 600
background_color = (255, 255, 255)
text_color = (0, 0, 0)
title_color = (34, 139, 34)  # Green color for the title

# Output path
output_path = "/home/jasvir/Music/Rosa/"

# Ensure the output directory exists
os.makedirs(output_path, exist_ok=True)

def create_image(text, font_path, font_size, output_file, text_color=text_color, bg_color=background_color):
    # Create an image with white background
    image = Image.new('RGB', (image_width, image_height), color=bg_color)
    draw = ImageDraw.Draw(image)

    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Wrap the text
    margin = 40
    offset = 50
    for line in textwrap.wrap(text, width=40):
        draw.text((margin, offset), line, font=font, fill=text_color)
        offset += font.getsize(line)[1] + 10

    # Save the image
    image.save(output_file)

# Create images for the title and each paragraph
create_image(title, title_font_path, title_font_size, os.path.join(output_path, "poem_title.png"), text_color=title_color)
for i, paragraph in enumerate(poem_paragraphs):
    create_image(paragraph, paragraph_font_path, paragraph_font_size, os.path.join(output_path, f"poem_paragraph_{i+1}.png"))
