import cv2
import numpy as np

def create_3d_effect(image_path, output_path, depth=10):
    # Load the image
    image = cv2.imread(image_path)
    height, width = image.shape[:2]

    # Create a blank image for the output
    output_image = np.zeros((height, width, 3), dtype=np.uint8)

    # Create a depth map (simple gradient)
    depth_map = np.zeros((height, width), dtype=np.float32)
    for i in range(height):
        depth_map[i, :] = (i / height) * depth

    # Apply the depth effect
    for i in range(height):
        shift = int(depth_map[i, 0])
        output_image[i, shift:width] = image[i, :width-shift]

    # Save the result
    cv2.imwrite(output_path, output_image)

# Define the paths
input_image_path = '/home/jasvir/Music/Data4/out (8).jpg'
output_image_path = '/home/jasvir/Music/Data4/3d_effect_image.jpg'

# Apply the 3D effect
create_3d_effect(input_image_path, output_image_path)
