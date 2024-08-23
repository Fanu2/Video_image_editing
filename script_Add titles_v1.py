from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def create_text_image(text, font_size=70, image_size=(1280, 720)):
    # Create an image with white background
    image = Image.new('RGB', image_size, color=(0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Load a font
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Calculate text size and position
    text_width, text_height = draw.textsize(text, font=font)
    text_x = (image_size[0] - text_width) // 2
    text_y = (image_size[1] - text_height) // 2

    # Draw the text
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))

    # Convert PIL image to numpy array
    return np.array(image)


# Path to the video file
video_file_path = "/home/jasvir/Music/Movie work/New video/nain.mp4"

# List of titles to add to the video
titles = [
    "You're my everything, Jodha",
    "Your love brightens my life",
    "Every moment with you is a treasure",
    "Your smile is my sunshine",
    "In your eyes, I find my home",
    "Together, we are unstoppable",
    "Your love completes me",
    "With you, life is a beautiful journey",
    "You're my dream come true",
    "Your love is my guiding star",
    "In your arms, I find peace",
    "You make my heart sing",
    "Every day with you is a blessing",
    "You're my reason to smile",
    "Your love is my strength",
    "Together, we create magic",
    "You're my soulmate",
    "Your love is my inspiration",
    "In your love, I find happiness",
    "Forever yours, Jodha"
]

# Load the video file
video_clip = VideoFileClip(video_file_path)
video_size = video_clip.size

# Duration for each title
title_duration = video_clip.duration / len(titles)

# Create a list of title clips
title_clips = []

for i, title in enumerate(titles):
    # Create text image
    text_image = create_text_image(title, font_size=70, image_size=video_size)
    txt_clip = ImageClip(text_image)
    txt_clip = (txt_clip
                .set_duration(title_duration)
                .set_position(('center', 'center'))
                .fadein(1)
                .fadeout(1))

    txt_clip = txt_clip.set_start(i * title_duration)
    title_clips.append(txt_clip)

# Combine the title clips with the video
final_clip = CompositeVideoClip([video_clip] + title_clips)

# Write the result to a file
output_file_path = "/home/jasvir/Music/Movie work/New video/nain_mille_with_titles.mp4"
final_clip.write_videofile(output_file_path, codec='libx264', audio_codec='aac')

print(f"Video with titles saved successfully: {output_file_path}")
