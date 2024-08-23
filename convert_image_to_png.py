from PIL import Image

def convert_image_to_png(input_path, output_path):
    with Image.open(input_path) as img:
        img.save(output_path, 'PNG')

# Example usage
convert_image_to_png('input.jpg', 'output.png')
