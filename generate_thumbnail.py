from PIL import Image

def generate_thumbnail(input_path, output_path, size):
    with Image.open(input_path) as img:
        img.thumbnail(size)
        img.save(output_path)

# Example usage
generate_thumbnail('input.jpg', 'thumbnail.jpg', (128, 128))
