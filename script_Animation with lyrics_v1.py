from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip, ImageClip, AudioFileClip, concatenate_videoclips
import os

# Function to create an image with text
def create_lyric_image(text, image_size=(1280, 720), bg_color=(255, 255, 255), text_color=(0, 0, 0), font_size=48, font_path="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
    image = Image.new('RGB', image_size, bg_color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)

    # Calculate text position
    text_width, text_height = draw.textsize(text, font=font)
    text_position = ((image_size[0] - text_width) // 2, (image_size[1] - text_height) // 2)

    # Draw text on image
    draw.text(text_position, text, fill=text_color, font=font)

    return image

# Romantic poem for "Lady of Roses"
poem_lines = [
    "In a garden of roses, you stand alone,",
    "A vision of beauty, in a world of stone.",
    "Your smile, a beacon, in the darkest night,",
    "Your touch, a whisper, that feels so right.",
    "With every glance, my heart does soar,",
    "In your presence, I need nothing more.",
    "You are the dream, I've waited for,",
    "My Lady of Roses, forevermore."
]

# Create lyric images and save them
lyric_images = []
for i, line in enumerate(poem_lines):
    lyric_image = create_lyric_image(line)
    temp_path = f"temp_lyric_image_{i}.png"
    lyric_image.save(temp_path)
    lyric_images.append(temp_path)

# Convert image files to moviepy ImageClips and set duration for each
lyric_clips = [ImageClip(img).set_duration(2) for img in lyric_images]

# Concatenate clips to form the final video
final_clip = concatenate_videoclips(lyric_clips, method="compose")

# Add audio
audio_file_path = "/home/jasvir/Music/Your Song .mp3"  # Replace with your audio file path
audio_clip = AudioFileClip(audio_file_path)
final_clip = final_clip.set_audio(audio_clip)

# Export the video
output_video_path = "/home/jasvir/Music/romantic_poem_video.mp4"
final_clip.write_videofile(output_video_path, codec='libx264', fps=24)

# Clean up temporary image files
for img_path in lyric_images:
    os.remove(img_path)
