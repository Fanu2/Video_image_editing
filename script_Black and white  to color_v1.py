from PIL import Image
import numpy as np
import os


def add_color_tint(image_path):
    try:
        # Load the black-and-white image
        image = Image.open(image_path).convert('RGB')

        # Convert image to numpy array
        image_array = np.array(image)

        # Define a color tint (e.g., light blue)
        tint_color = np.array([173, 216, 230], dtype=np.uint8)  # RGB for light blue

        # Create a color tint array
        tint_array = np.full_like(image_array, tint_color)

        # Blend the original image with the color tint
        tinted_image_array = np.clip(image_array * 0.7 + tint_array * 0.3, 0, 255).astype(np.uint8)

        # Convert back to Image object
        tinted_image = Image.fromarray(tinted_image_array)

        # Save the tinted image to the same path
        tinted_image.save(image_path)
        print(f"Image saved to {image_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    # Prompt user for the input image path
    input_image_path = input("Enter the path to the black-and-white image: ")

    # Check if file exists
    if not os.path.isfile(input_image_path):
        print("File not found. Please check the path and try again.")
        return

    # Process the image
    add_color_tint(input_image_path)


if __name__ == "__main__":
    main()
