import cv2
import numpy as np

def cartoonize_image(input_image_path, output_image_path):
    # Read the image
    img = cv2.imread(input_image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply bilateral filter to reduce noise while keeping edges sharp
    gray = cv2.bilateralFilter(gray, 7, 50, 50)

    # Detect edges in the image and threshold it
    edges = cv2.Laplacian(gray, cv2.CV_8U, ksize=5)
    ret, edges = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)

    # Apply a median blur to the thresholded image
    edges = cv2.medianBlur(edges, 5)

    # Create a cartoonized version by combining edges with a color image
    cartoon = cv2.bitwise_and(img, img, mask=edges)

    # Save or display the cartoonized image
    cv2.imwrite(output_image_path, cartoon)
    cv2.imshow("Cartoonized Image", cartoon)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage:
input_image_path = "/home/jasvir/Music/Image/1.jpg"
output_image_path = "/home/jasvir/Music/Image/cartoonized_image.jpg"

cartoonize_image(input_image_path, output_image_path)
