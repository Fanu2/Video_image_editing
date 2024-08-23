from PIL import Image
import imageio
import os
import tempfile


def resize_image(image_path, target_size=(800, 600)):
    img = Image.open(image_path)
    img_resized = img.resize(target_size, Image.ANTIALIAS)  # Resize to target size with anti-aliasing
    return img_resized


def create_animated_gif(image_folder, output_gif, duration=0.5):
    images = []
    temp_files = []

    for filename in sorted(os.listdir(image_folder)):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            file_path = os.path.join(image_folder, filename)
            img_resized = resize_image(file_path)  # Resize each image to ensure uniform dimensions

            # Save resized image to a temporary file
            temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            temp_files.append(temp_file.name)
            img_resized.save(temp_file.name)

            # Append the temporary file path to the images list
            images.append(temp_file.name)

    # Create animated GIF from the list of temporary file paths
    imageio.mimsave(output_gif, [imageio.imread(image) for image in images], duration=duration)

    # Clean up temporary files
    for temp_file in temp_files:
        os.remove(temp_file)


# Example usage:
image_folder = '/home/jasvir/Documents/Slide show6/'
output_gif = '/home/jasvir/Documents/Slide show6.gif'

create_animated_gif(image_folder, output_gif, duration=0.5)
