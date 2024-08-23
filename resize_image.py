from PIL import Image

def resize_image(input_path, output_path, size):
    with Image.open(input_path) as img:
        img = img.resize(size)
        img.save(output_path)

# Example usage
resize_image('input.jpg', 'output_resized.jpg', (800, 600))
