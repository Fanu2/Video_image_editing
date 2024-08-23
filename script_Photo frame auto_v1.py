import cv2
import numpy as np

def add_photo_frame(image_path, output_path, frame_thickness=30, frame_color=(0, 0, 0)):
    # Read the image
    img = cv2.imread(image_path)
    height, width = img.shape[:2]

    # Calculate the size of the frame template
    frame_height = height + 2 * frame_thickness
    frame_width = width + 2 * frame_thickness

    # Create a frame template
    frame_template = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
    frame_template[:, :] = frame_color

    # Insert the image into the frame template
    frame_template[frame_thickness:frame_thickness + height, frame_thickness:frame_thickness + width] = img

    # Save the output image
    cv2.imwrite(output_path, frame_template)

    # Display the image with frame (optional)
    cv2.imshow("Image with Photo Frame", frame_template)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage:
image_path = "/home/jasvir/Music/Image/1.jpg"
output_path = "/home/jasvir/Music/Image/1_with_photo_frame.jpg"

# Call the function to add a photo frame and save the result
add_photo_frame(image_path, output_path)
