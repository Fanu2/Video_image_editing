import cv2
import numpy as np

def mirror_image(image_path, output_path, mode='horizontal'):
    # Read the image
    img = cv2.imread(image_path)

    # Mirror the image based on mode
    if mode == 'horizontal':
        mirrored_img = cv2.flip(img, 1)  # 1 for horizontal flip
    elif mode == 'vertical':
        mirrored_img = cv2.flip(img, 0)  # 0 for vertical flip
    else:
        raise ValueError("Invalid mode. Use 'horizontal' or 'vertical'.")

    # Save the mirrored image
    cv2.imwrite(output_path, mirrored_img)

    # Display the original and mirrored images (optional)
    cv2.imshow("Original Image", img)
    cv2.imshow("Mirrored Image", mirrored_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage:
image_path = "/home/jasvir/Music/Image/1.jpg"
output_path_horizontal = "/home/jasvir/Music/Image/1_horizontal_mirror.jpg"
output_path_vertical = "/home/jasvir/Music/Image/1_vertical_mirror.jpg"

# Mirror horizontally
mirror_image(image_path, output_path_horizontal, mode='horizontal')

# Mirror vertically
mirror_image(image_path, output_path_vertical, mode='vertical')
