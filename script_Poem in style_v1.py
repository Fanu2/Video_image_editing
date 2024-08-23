from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import textwrap


def create_stylish_text(text, font_path, output_path, image_size=(1920, 1080), font_size=60, color="white",
                        bgcolor="black"):
    # Create a new image with a solid background
    image = Image.new("RGB", image_size, bgcolor)
    draw = ImageDraw.Draw(image)

    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Wrap text
    wrapped_text = textwrap.fill(text, width=40)

    # Calculate text size and position
    text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    text_x = (image_size[0] - text_width) // 2
    text_y = (image_size[1] - text_height) // 2

    # Apply shadow effect
    shadow_offset = 5
    shadow_color = "grey"
    draw.text((text_x + shadow_offset, text_y + shadow_offset), wrapped_text, font=font, fill=shadow_color)

    # Apply outline effect
    outline_color = "black"
    outline_range = 1
    for x in range(-outline_range, outline_range + 1):
        for y in range(-outline_range, outline_range + 1):
            draw.text((text_x + x, text_y + y), wrapped_text, font=font, fill=outline_color)

    # Draw the main text
    draw.text((text_x, text_y), wrapped_text, font=font, fill=color)

    # Apply gradient effect to the text (optional)
    gradient = Image.new("L", (1, text_height), color=0xFF)
    for y in range(text_height):
        gradient.putpixel((0, y), int(255 * (y / text_height)))
    alpha = gradient.resize((text_width, text_height))
    black_text = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 255))
    draw_text = ImageDraw.Draw(black_text)
    draw_text.text((0, 0), wrapped_text, font=font, fill=color)
    gradient_text = Image.composite(black_text, Image.new("RGBA", black_text.size, (0, 0, 0, 0)), alpha)
    image.paste(gradient_text, (text_x, text_y), gradient_text)

    # Apply a filter to make the text more stylish
    image = image.filter(ImageFilter.SMOOTH_MORE)

    # Save the image
    image.save(output_path)


# Define the paths and text
poem_lines = [
    "Lady of Roses",
    "In the highlands where the green abounds,\nLives a lady with roses all around.\nPassion blooms in her garden so fair,\nA testament to her loving care.",
    "With petals soft and colors bright,\nHer roses dance in the morning light.\nEach bloom whispers tales untold,\nOf a heart that's pure and bold.",
    "In her garden, love and nature meet,\nA sanctuary of peace, so sweet.\nHer hands nurture each fragile stem,\nIn her care, they find their gem.",
    "The Lady of Roses, kind and wise,\nSees the world through gentle eyes.\nHer roses, like her, stand tall and true,\nA symbol of love in all they do.",
    "With a heart as green as the leaves she tends,\nHer spirit, like the garden, never ends.\nLady of Roses, in her domain,\nWhere love and beauty forever reign."
]

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Update with your font path
output_folder = "/home/jasvir/Music/Rosa/"

# Ensure the output folder exists
import os

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Create images for each line of the poem
for i, line in enumerate(poem_lines):
    output_path = os.path.join(output_folder, f"poem_line_{i + 1}.png")
    create_stylish_text(line, font_path, output_path)
