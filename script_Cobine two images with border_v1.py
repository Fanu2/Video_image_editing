from PIL import Image, ImageOps

def resize_images_to_same_size(image1, image2, size):
    # Resize both images to the specified size
    img1_resized = image1.resize(size, Image.ANTIALIAS)
    img2_resized = image2.resize(size, Image.ANTIALIAS)
    return img1_resized, img2_resized

def combine_images_with_border(image1_path, image2_path, output_path, size, border_size=10, background_color=(255, 255, 255)):
    # Open the images
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)

    # Resize images to the same size
    img1_resized, img2_resized = resize_images_to_same_size(img1, img2, size)

    # Calculate the size for the new image
    total_width = img1_resized.width + img2_resized.width + 3 * border_size
    max_height = max(img1_resized.height, img2_resized.height) + 2 * border_size

    # Create a new image with a white background
    new_image = Image.new('RGB', (total_width, max_height), background_color)

    # Paste the first image onto the new image with a border
    new_image.paste(ImageOps.expand(img1_resized, border=border_size, fill=background_color), (border_size, border_size))

    # Paste the second image onto the new image with a border
    new_image.paste(ImageOps.expand(img2_resized, border=border_size, fill=background_color), (img1_resized.width + 2 * border_size, border_size))

    # Save the final image
    new_image.save(output_path)

# Example usage
image1_path = '/home/jasvir/Music/Combined/1.jpg'
image2_path = '/home/jasvir/Music/Combined/2.jpg'
output_path = '/home/jasvir/Music/Combined/combined_image.jpg'
# Define the size to which both images will be resized
resize_size = (300, 300)  # Example size (width, height)
combine_images_with_border(image1_path, image2_path, output_path, size=resize_size, border_size=10, background_color=(255, 255, 255))
