from PIL import Image, ImageOps

def apply_sepia_filter(input_path, output_path):
    with Image.open(input_path) as img:
        sepia_img = ImageOps.colorize(img.convert('L'), '#704214', '#C0C0C0')
        sepia_img.save(output_path)

# Example usage
apply_sepia_filter('input.jpg', 'output_sepia.jpg')
