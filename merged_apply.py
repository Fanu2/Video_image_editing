

# ==== Start of apply_filter.py ====

from PIL import Image, ImageFilter

def apply_filter(input_path, output_path, filter_type):
    with Image.open(input_path) as img:
        if filter_type == 'BLUR':
            img = img.filter(ImageFilter.BLUR)
        elif filter_type == 'CONTOUR':
            img = img.filter(ImageFilter.CONTOUR)
        img.save(output_path)

# Example usage
apply_filter('input.jpg', 'output_blur.jpg', 'BLUR')


# ==== Start of apply_gaussian_blur.py ====

from PIL import Image, ImageFilter

def apply_gaussian_blur(input_path, output_path, radius):
    with Image.open(input_path) as img:
        blurred_img = img.filter(ImageFilter.GaussianBlur(radius))
        blurred_img.save(output_path)

# Example usage
apply_gaussian_blur('input.jpg', 'output_blur.jpg', 5)


# ==== Start of apply_sepia_filter.py ====

from PIL import Image, ImageOps

def apply_sepia_filter(input_path, output_path):
    with Image.open(input_path) as img:
        sepia_img = ImageOps.colorize(img.convert('L'), '#704214', '#C0C0C0')
        sepia_img.save(output_path)

# Example usage
apply_sepia_filter('input.jpg', 'output_sepia.jpg')


# ==== Start of apply_sepia_filter_to_video.py ====

from moviepy.editor import VideoFileClip
from moviepy.video.fx import colorx

def apply_sepia_filter(video_path, output_path, intensity):
    video = VideoFileClip(video_path)
    sepia_video = colorx(video, intensity)
    sepia_video.write_videofile(output_path)

# Example usage
apply_sepia_filter('input.mp4', 'output_sepia.mp4', 1.5)


# ==== Start of merged_apply.py ====

