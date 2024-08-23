from PIL import Image, ImageOps

def add_border(input_path, output_path, border_size):
    with Image.open(input_path) as img:
        bordered_img = ImageOps.expand(img, border=border_size, fill='black')
        bordered_img.save(output_path)

# Example usage
add_border('input.jpg', 'output_bordered.jpg', 10)
