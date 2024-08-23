from PIL import Image, ImageOps, ImageEnhance

def stylize_image(input_image_path, output_image_path):
    # Open the image file
    image = Image.open(input_image_path)

    # Convert image to grayscale
    grayscale_image = ImageOps.grayscale(image)
    grayscale_image.save(output_image_path.replace(".jpg", "_grayscale.jpg"))

    # Add a sepia tone effect
    sepia_image = apply_sepia(image)
    sepia_image.save(output_image_path.replace(".jpg", "_sepia.jpg"))

    # Apply posterization effect
    posterized_image = apply_posterization(image)
    posterized_image.save(output_image_path.replace(".jpg", "_posterized.jpg"))

def apply_sepia(image):
    width, height = image.size
    pixels = image.load()

    for py in range(height):
        for px in range(width):
            r, g, b = image.getpixel((px, py))
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            if tr > 255:
                tr = 255
            if tg > 255:
                tg = 255
            if tb > 255:
                tb = 255
            pixels[px, py] = (tr, tg, tb)

    return image

def apply_posterization(image):
    posterized_image = ImageOps.posterize(image, 4)  # Reduce to 4 levels of color per channel
    return posterized_image

# Example usage:
input_image_path = "/home/jasvir/Music/Image/1.jpg"
output_image_path = "/home/jasvir/Music/Image/stylized_image.jpg"

stylize_image(input_image_path, output_image_path)
