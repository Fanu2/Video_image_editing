from moviepy.editor import ImageSequenceClip
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import platform

def get_default_font(size=70):
    """Return a default font. Try common system fonts, fallback to PIL default."""
    try:
        if platform.system() == "Windows":
            font_path = "C:\\Windows\\Fonts\\Arial.ttf"
        elif platform.system() == "Darwin":  # macOS
            font_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
        else:  # Linux and others
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        return ImageFont.truetype(font_path, size=size)
    except IOError:
        print("Warning: Custom font not found, using default font.")
        return ImageFont.load_default()

def add_text_to_image(image_path, text):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    font = get_default_font(size=70)
    
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    text_x = (img.width - text_width) // 2
    text_y = img.height - text_height - 20  # Adjust vertical position
    
    draw.text((text_x, text_y), text, font=font, fill='white')
    return np.array(img)

def resize_image(img_array, target_size=(1920, 1080)):
    img_resized = Image.fromarray(img_array).resize(target_size)
    return np.array(img_resized)

def create_animation(input_folder, output_video, text="Love u Jodha"):
    if not os.path.isdir(input_folder):
        raise FileNotFoundError(f"Input folder not found: {input_folder}")

    file_list = sorted([f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.png'))])
    if not file_list:
        raise ValueError(f"No images found in {input_folder}")

    clips = []
    for filename in file_list:
        image_path = os.path.join(input_folder, filename)
        img_with_text = add_text_to_image(image_path, text)
        img_resized = resize_image(img_with_text)
        clips.append(img_resized)

    fps = 24
    duration = len(clips) / fps
    video_clip = ImageSequenceClip(clips, fps=fps).set_duration(duration)
    looped_clip = video_clip.loop().set_duration(duration)
    looped_clip.write_videofile(output_video, codec='libx264', fps=fps)
    print(f"Animation saved as {output_video}")

# Usage example (remove these lines if integrating in another script)
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create video animation from images with text overlay.")
    parser.add_argument("--input_folder", type=str, required=True, help="Path to folder containing images.")
    parser.add_argument("--output_video", type=str, required=True, help="Path to save output video.")
    parser.add_argument("--text", type=str, default="Love u Jodha", help="Text to overlay on images.")
    args = parser.parse_args()

    create_animation(args.input_folder, args.output_video, args.text)
