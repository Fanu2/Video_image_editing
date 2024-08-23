from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# Poem text
title = "Whispers of Rosa"
poem_paragraphs = [
    "In a garden where the roses bloom so bright,\nLives a tale of love, pure as morning light.\nRosa, with petals soft and fair,\nA symbol of romance, beyond compare.",
    "Her fragrance dances on the evening breeze,\nA whisper of love among the trees.\nEach petal blushes with a crimson hue,\nA testament to a love so true.",
    "In the moonlit night, where shadows play,\nRosa’s beauty takes my breath away.\nHer thorns protect, yet never harm,\nA gentle guardian with endless charm.",
    "Beneath the stars, we sit hand in hand,\nLost in a dream, in a love so grand.\nHer laughter, a melody, sweet and clear,\nIn her embrace, I have nothing to fear.",
    "With every dawn, our love renews,\nIn the light of day, with skies so blue.\nRosa, my heart, my soul's delight,\nIn your love, I find my light.",
    "In the silence, where secrets keep,\nOur love’s whispers, tender and deep.\nRosa, with you, my dreams take flight,\nIn this garden of love, everything feels right."
]

# Font settings
title_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
paragraph_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
title_font_size = 48 
paragraph_font_size = 36

# Image settings
image_width = 800
image_height = 600
background_color = (255, 255, 255)
text_color = (0, 0, 0)
title_color = (255, 0, 0)  # Red color for the title

# Output path
output_path = "/home/jasvir/Music/Rosa1/"

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
