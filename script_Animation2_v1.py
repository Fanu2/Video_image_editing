import os
from PIL import Image
import imageio


def create_animated_gif(image_folder, output_gif, duration=0.5):
    images = []

    # Get a list of all image files in the folder
    for file_name in sorted(os.listdir(image_folder)):
        if file_name.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            file_path = os.path.join(image_folder, file_name)

            # Open the image
            image = Image.open(file_path)

            # Resize the image to a fixed size (let's use 800x600 for example)
            image_resized = image.resize((800, 600), Image.LANCZOS)

            # Convert the image to a format suitable for imageio
            image_resized = image_resized.convert('RGB')

            # Append the image to the list
            images.append(image_resized)

    # Save the images as an animated GIF
    imageio.mimsave(output_gif, [image for image in images], duration=duration)


# Define the folder path and output gif path
image_folder = "/home/jasvir/Documents/Slide show6/"
output_gif = "/home/jasvir/Documents/Slide show6.gif"

# Call the function
create_animated_gif(image_folder, output_gif, duration=1.5)
