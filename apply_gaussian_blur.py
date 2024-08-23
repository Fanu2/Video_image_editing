from PIL import Image, ImageFilter

def apply_gaussian_blur(input_path, output_path, radius):
    with Image.open(input_path) as img:
        blurred_img = img.filter(ImageFilter.GaussianBlur(radius))
        blurred_img.save(output_path)

# Example usage
apply_gaussian_blur('input.jpg', 'output_blur.jpg', 5)
