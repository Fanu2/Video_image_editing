from PIL import Image, ImageDraw, ImageFont

def create_image_with_text(output_path, text="Princess Jodha", width=800, height=400, background_color=(255, 255, 255), text_color=(0, 255, 0), font_size=50):
    # Create a new image with the specified background color
    image = Image.new('RGB', (width, height), color=background_color)

    # Initialize the drawing context
    draw = ImageDraw.Draw(image)

    # Load a font
    try:
        # Specify the path to a truetype font file available on your MX Linux system
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Update this to your font path
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        # Fall back to the default PIL font if the specified font is not available
        font = ImageFont.load_default()

    # Calculate the width and height of the text to be added
    text_width, text_height = draw.textsize(text, font=font)

    # Calculate X, Y position of the text
    x = (width - text_width) / 2
    y = (height - text_height) / 2

    # Add text to image
    draw.text((x, y), text, fill=text_color, font=font)

    # Save the image
    image.save(output_path)
    print(f"Image saved to {output_path}")

# Define the output path for the image
output_path = "/home/jasvir/Music/Data/Love_you_Jassi2.png"

# Call the function to create the image
create_image_with_text(output_path)
