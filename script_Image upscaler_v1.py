import cv2
import os


def upscale_images(input_folder, output_folder, scale_factor=2):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the list of all files in the input folder
    files = os.listdir(input_folder)

    # Filter out files that are not images
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]

    for image_file in image_files:
        # Construct the full file path
        input_path = os.path.join(input_folder, image_file)
        output_path = os.path.join(output_folder, image_file)

        # Read the image
        image = cv2.imread(input_path)

        if image is None:
            print(f"Error reading image {input_path}")
            continue

        # Get the dimensions of the image
        height, width = image.shape[:2]

        # Calculate the new dimensions
        new_dimensions = (int(width * scale_factor), int(height * scale_factor))

        # Resize the image
        upscaled_image = cv2.resize(image, new_dimensions, interpolation=cv2.INTER_CUBIC)

        # Save the upscaled image
        cv2.imwrite(output_path, upscaled_image)

        print(f"Upscaled image saved to {output_path}")


# Example usage
input_folder = '/home/jasvir/Music/Movie work/studio/'
output_folder = '/home/jasvir/Music/Movie work/studio/upscaled/'
scale_factor = 2  # Upscale by a factor of 2

upscale_images(input_folder, output_folder, scale_factor)
