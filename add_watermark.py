from PIL import Image

def add_watermark(image_path, watermark_path, output_path, position):
    with Image.open(image_path) as img:
        with Image.open(watermark_path) as watermark:
            img.paste(watermark, position, watermark)
            img.save(output_path)

# Example usage
add_watermark('input.jpg', 'watermark.png', 'output_watermarked.jpg', (50, 50))
