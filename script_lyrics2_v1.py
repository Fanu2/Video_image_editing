from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy.editor import ImageSequenceClip

# Function to create an image with text
def create_lyric_image(text, image_size=(1280, 720), bg_color=(255, 255, 255), text_color=(0, 0, 0), font_size=48):
    image = Image.new('RGB', image_size, bg_color)
    draw = ImageDraw.Draw(image)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Replace with your chosen DejaVu font file path
    font = ImageFont.truetype(font_path, font_size)

    # Calculate text position
    text_width, text_height = draw.textsize(text, font=font)
    text_position = ((image_size[0] - text_width) // 2, (image_size[1] - text_height) // 2)

    # Draw text on image
    draw.text(text_position, text, fill=text_color, font=font)

    return image

# Example lyrics
lyrics = [
    "Darling, just hold my hand",
    "Be my girl, I'll be your man",
    "I see my future in your eyes",
    "There goes my heart beating",
    "'Cause you are the reason",
    "I'm losing my sleep",
    "Please come back now"
    
]

# Create lyric images
lyric_images = []
for lyric in lyrics:
    lyric_image = create_lyric_image(lyric)
    lyric_images.append(np.array(lyric_image))  # Convert Pillow image to NumPy array

# Create a video clip from images
video_clip = ImageSequenceClip(lyric_images, fps=1)  # Adjust the fps according to your preference

# Export the video
output_video_path = "/home/jasvir/Music/video.mp4"
video_clip.write_videofile(output_video_path, codec='libx264')
