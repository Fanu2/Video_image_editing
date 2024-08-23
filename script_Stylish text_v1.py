from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

def create_stylish_text(text, font_path, output_path, image_size=(800, 600), font_size=100, color="white", bgcolor="black"):
    # Create a new image with a solid background
    image = Image.new("RGB", image_size, bgcolor)
    draw = ImageDraw.Draw(image)

    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Calculate text size and position
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    text_x = (image_size[0] - text_width) // 2
    text_y = (image_size[1] - text_height) // 2

    # Apply shadow effect
    shadow_offset = 10
    shadow_color = "grey"
    draw.text((text_x + shadow_offset, text_y + shadow_offset), text, font=font, fill=shadow_color)

    # Apply outline effect
    outline_color = "black"
    outline_range = 2
    for x in range(-outline_range, outline_range+1):
        for y in range(-outline_range, outline_range+1):
            draw.text((text_x + x, text_y + y), text, font=font, fill=outline_color)

    # Draw the main text
    draw.text((text_x, text_y), text, font=font, fill=color)

    # Apply gradient effect to the text (optional)
    gradient = Image.new("L", (1, text_height), color=0xFF)
    for y in range(text_height):
        gradient.putpixel((0, y), int(255 * (y / text_height)))
    alpha = gradient.resize((text_width, text_height))
    black_text = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 255))
    draw_text = ImageDraw.Draw(black_text)
    draw_text.text((0, 0), text, font=font, fill=color)
    gradient_text = Image.composite(black_text, Image.new("RGBA", black_text.size, (0, 0, 0, 0)), alpha)
    image.paste(gradient_text, (text_x, text_y), gradient_text)

    # Apply a filter to make the text more stylish
    image = image.filter(ImageFilter.SMOOTH_MORE)

    # Save the image
    image.save(output_path)

# Define the paths and text
text = "Love u Jodha"
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Update with your font path
output_path = "/home/jasvir/Music/Jodha/stylish_text.png"

# Create stylish text with effects
create_stylish_text(text, font_path, output_path)
