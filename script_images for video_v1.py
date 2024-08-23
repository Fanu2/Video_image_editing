from PIL import Image, ImageDraw, ImageFont
import os

def create_image_with_text(text, output_path, resolution=(1920, 1080), font_path=None, font_size=60, text_color=(255, 255, 255)):
    # Create a blank image with the specified resolution
    image = Image.new('RGB', resolution, color=(0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Load a font
    if font_path is None:
        font = ImageFont.load_default()
    else:
        font = ImageFont.truetype(font_path, font_size)

    # Calculate text size and position using textbbox
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((resolution[0] - text_width) // 2, (resolution[1] - text_height) // 2)

    # Add text to image
    draw.text(position, text, font=font, fill=text_color)

    # Save the image
    image.save(output_path)
    print(f"Image saved to {output_path}")

# Define the text and output paths
texts = [
    "Title: Lady of Roses 🌹",
    "In the highlands of Mizoram, she stands,",
    "A beacon of passion, with gentle hands.",
    "Nature lover, award-winning teacher,",
    "Her kindness and care, a beautiful feature.",
    "Protecting greenery with a heart so green,",
    "In her rose garden, a serene scene.",
    "Lady of Roses, a name so sweet,",
    "Her compassion and grace, a remarkable feat.",
    "Helping others, a social delight,",
    "Sympathetic and caring, day and night.",
    "A national award, for excellence received,",
    "In her love for nature, she's deeply believed.",
    "Green is her color, vibrant and pure,",
    "Her dedication to nature will always endure.",
    "In the highlands, where roses bloom,",
    "Her presence dispels any gloom.",
    "Lady of Roses, with a heart so true,",
    "Your passion and kindness inspire us too.",
    "In every rose, your love does show,",
    "A symbol of care, helping us grow."
]

output_folder = "/home/jasvir/Music/Rosa/"

# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Create images for each text
for i, text in enumerate(texts):
    output_path = os.path.join(output_folder, f"image_{i+1}.jpg")
    create_image_with_text(text, output_path, font_path="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")

print("Images created successfully.")
