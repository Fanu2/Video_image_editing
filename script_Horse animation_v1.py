import cv2
import numpy as np
import os
import random
from moviepy.editor import ImageSequenceClip


# Define a function to colorize an image using a specified color map
def colorize_image(input_path, output_path, color_map):
    # Load the grayscale image
    gray_image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    # Apply the color map
    color_image = cv2.applyColorMap(gray_image, color_map)

    # Save the colorized image
    cv2.imwrite(output_path, color_image)


def create_animation(image_dir, output_video_path, fps=30, duration=60):
    # Get list of colorized images
    image_files = [os.path.join(image_dir, f) for f in sorted(os.listdir(image_dir)) if
                   f.startswith('colorized_') and f.endswith('.png')]

    if not image_files:
        raise ValueError("No colorized images found in the specified directory.")

    # Create a video clip from the images
    clip = ImageSequenceClip(image_files, fps=fps)

    # Ensure the video is not longer than the specified duration
    clip = clip.subclip(0, min(duration, clip.duration))

    # Write the video file
    clip.write_videofile(output_video_path, codec='libx264')


def main():
    # Paths
    input_dir = '/home/jasvir/Music/Movie work/Black and white/'
    output_dir = input_dir  # Output path same as input directory

    # List of color maps available in OpenCV
    COLOR_MAPS = [
        cv2.COLORMAP_JET,
        cv2.COLORMAP_HSV,
        cv2.COLORMAP_RAINBOW,
        cv2.COLORMAP_OCEAN,
        cv2.COLORMAP_SUMMER,
        cv2.COLORMAP_SPRING,
        cv2.COLORMAP_AUTUMN,
        cv2.COLORMAP_WINTER,
        cv2.COLORMAP_BONE,
        cv2.COLORMAP_COOL,
        cv2.COLORMAP_HOT,
        cv2.COLORMAP_PINK,
        cv2.COLORMAP_PARULA
    ]

    # Get list of images in the input directory
    input_images = [os.path.join(input_dir, img) for img in os.listdir(input_dir) if
                    img.endswith(('.png', '.jpg', '.jpeg'))]

    # Check if there are enough images
    if len(input_images) < 30:
        raise ValueError("Not enough images found in the specified directory.")

    # Ensure at least 30 color maps are used by reusing if necessary
    if len(COLOR_MAPS) < 30:
        print("Warning: Less than 30 color maps available. Reusing color maps.")

    # Generate 30 colorized images
    for i in range(30):
        img_path = input_images[i % len(input_images)]  # Cycle through images
        color_map = COLOR_MAPS[i % len(COLOR_MAPS)]  # Cycle through color maps

        # Define output image path
        output_image_path = os.path.join(output_dir, f'colorized_{i + 1}.png')

        # Colorize the image
        colorize_image(img_path, output_image_path, color_map)

    # Define output video path
    output_video_path = os.path.join(output_dir, 'colorized_animation.mp4')

    # Create animation
    create_animation(output_dir, output_video_path, fps=3, duration=60)

    print(f"Animation created and saved to {output_video_path}")


if __name__ == "__main__":
    main()
