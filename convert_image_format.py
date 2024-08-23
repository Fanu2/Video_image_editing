from PIL import Image

def convert_image_format(input_path, output_path, format):
    with Image.open(input_path) as img:
        img.save(output_path, format=format)

# Example usage
convert_image_format('input.png', 'output.jpg', 'JPEG')
