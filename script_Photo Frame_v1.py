import cv2
import numpy as np

def add_border(image_path, output_path, border_size=30, border_color=(255, 255, 255)):
    # Read the image
    img = cv2.imread(image_path)

    # Get image dimensions
    height, width = img.shape[:2]

    # Create a border of specified size and color
    bordered_img = cv2.copyMakeBorder(
        img,
        border_size,  # top
        border_size,  # bottom
        border_size,  # left
        border_size,  # right
        cv2.BORDER_CONSTANT,
        value=border_color
    )

    # Add decorative elements or patterns to the border (optional)
    # Example: Add a frame design
    frame_design = cv2.imread('/phome/jasvir/Music/Image/frame_design.png')  # Replace with your frame design
    if frame_design is not None:
        frame_height, frame_width = frame_design.shape[:2]
        # Resize frame design to match the dimensions of the bordered image
        frame_design_resized = cv2.resize(frame_design, (width + 2 * border_size, height + 2 * border_size))
        # Overlay the frame design onto the bordered image
        bordered_img[:frame_height, :frame_width] = frame_design_resized

    # Save the output image
    cv2.imwrite(output_path, bordered_img)

    # Display the image with border (optional)
    cv2.imshow("Image with Border", bordered_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage:
image_path = "/home/jasvir/Music/Image/1.jpg"
output_path = "/home/jasvir/Music/Image/1_with_border.jpg"

# Call the function to add a border and save the result
add_border(image_path, output_path, border_size=30, border_color=(255, 255, 255))
