from PIL import Image, ImageFilter

def apply_filter(input_path, output_path, filter_type):
    with Image.open(input_path) as img:
        if filter_type == 'BLUR':
            img = img.filter(ImageFilter.BLUR)
        elif filter_type == 'CONTOUR':
            img = img.filter(ImageFilter.CONTOUR)
        img.save(output_path)

# Example usage
apply_filter('input.jpg', 'output_blur.jpg', 'BLUR')
