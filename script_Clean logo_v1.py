from PIL import Image, ImageDraw, ImageFont

def create_clean_modern_logo(text, font_path, output_path):
    # Define image size and background color
    image_size = (800, 200)
    background_color = (255, 255, 255)
    text_color = (0, 0, 255)  # Blue

    # Create a new image
    image = Image.new('RGB', image_size, background_color)
    draw = ImageDraw.Draw(image)

    # Load the font and calculate text size
    font = ImageFont.truetype(font_path, 100)
    text_size = draw.textsize(text, font=font)
    text_position = ((image_size[0] - text_size[0]) // 2, (image_size[1] - text_size[1]) // 2)

    # Draw the text
    draw.text(text_position, text, fill=text_color, font=font)

    # Save the image
    image.save(output_path)

# Usage
create_clean_modern_logo(
    text="DJ Blue",
    font_path="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    output_path="/home/jasvir/Pictures/pic1/clean_modern_logo.png"
)
