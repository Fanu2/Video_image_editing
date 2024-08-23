from PIL import Image, ImageDraw, ImageFont

def overlay_text(input_path, output_path, text, position, font_size):
    with Image.open(input_path) as img:
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf', font_size)
        draw.text(position, text, font=font, fill='white')
        img.save(output_path)

# Example usage
overlay_text('input.jpg', 'output_text.jpg', 'Hello World', (50, 50), 40)
