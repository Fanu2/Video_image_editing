from PIL import Image
import imageio

def create_gif(input_image, output_gif, duration=0.5, loops=0):
    # Open the input image using Pillow
    img = Image.open(input_image)

    # Create a list of images (frames) for the GIF
    images = [img]  # Start with the original image
    num_frames = 10  # Number of frames to duplicate (adjust as needed)

    for _ in range(num_frames):
        images.append(img.copy())  # Duplicate the image multiple times

    # Save the frames as a GIF using imageio
    imageio.mimsave(output_gif, images, duration=duration, loop=loops)

# Example usage:
input_image = '/home/jasvir/Documents/abc.jpg'
output_gif = '/home/jasvir/Documents/output.gif'

create_gif(input_image, output_gif, duration=0.5, loops=0)
