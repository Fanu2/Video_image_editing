from PIL import Image, ImageEnhance

def adjust_brightness(input_path, output_path, factor):
    with Image.open(input_path) as img:
        enhancer = ImageEnhance.Brightness(img)
        img_enhanced = enhancer.enhance(factor)
        img_enhanced.save(output_path)

# Example usage
adjust_brightness('input.jpg', 'output_bright.jpg', 1.5)
