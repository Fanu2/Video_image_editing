from PIL import Image, ImageDraw, ImageFont

def create_playful_energetic_logo(text, font_path, output_path):
    # Define image size and background color
    image_size = (800, 300)
    background_color = (255, 255, 255)
    text_color = (255, 0, 0)  # Red
    splash_color = (0, 255, 0)  # Green

    # Create a new image
    image = Image.new('RGB', image_size, background_color)
    draw = ImageDraw.Draw(image)

    # Load the font and calculate text size
    font = ImageFont.truetype(font_path, 100)
    text_size = draw.textsize(text, font=font)
    text_position = ((image_size[0] - text_size[0]) // 2, (image_size[1] - text_size[1]) // 2)

    # Draw the text
    draw.text(text_position, text, fill=text_color, font=font)

    # Add a playful splash element
    splash_size = (150, 150)
    splash_position = (text_position[0] + text_size[0] + 10, text_position[1] - 30)
    draw.ellipse([splash_position, (splash_position[0] + splash_size[0], splash_position[1] + splash_size[1])], fill=splash_color)

    # Save the image
    image.save(output_path)

# Usage
create_playful_energetic_logo(
    text="DJ Blue",
    font_path="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    output_path="/home/jasvir/Pictures/pic1/playful_energetic_logo.png"
)
