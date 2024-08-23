from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy.editor import ImageSequenceClip

# Function to create an image with text
def create_lyric_image(text, image_size=(1280, 720), bg_color=(255, 255, 255), text_color=(0, 0, 0), font_size=48):
    image = Image.new('RGB', image_size, bg_color)
    draw = ImageDraw.Draw(image)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Replace with your font file path
    font = ImageFont.truetype(font_path, font_size)

    # Calculate text position
    text_width, text_height = draw.textsize(text, font=font)
    text_position = ((image_size[0] - text_width) // 2, (image_size[1] - text_height) // 2)

    # Draw text on image
    draw.text(text_position, text, fill=text_color, font=font)

    return image

# Romantic poem for Fanu
poem = [
   
    "In the garden where roses bloom,",
    "Your presence turns it into a sweet perfume.",
    "Each petal whispers of your grace,",
    "In every blush, I see your gentle embrace.",
    "",
    "Lady of Roses, your beauty untold,",
    "In your eyes, secrets of love unfold.",
    "With each glance, my heart skips a beat,",
    "Your smile, a melody, so tender and sweet.",
    "",
    "Among the roses, you stand apart,",
    "A masterpiece of love's finest art.",
    "In your heart, a garden of dreams,",
    "Where love blooms eternal, like sunlit streams.",
    "",
    "Your laughter, like petals in the breeze,",
    "Your touch, the warmth of summer seas.",
    "Lady of Roses, in your soul divine,",
    "Forever, in your love, I am entwined.",
    "",
    "Through every season, through every dawn,",
    "With you, my love, I belong.",
    "In the garden where roses grow,",
    "With you, forever, my heart shall know.",
    "",
    "Lady of Roses, my love, my muse,",
    "In your embrace, all dreams fuse.",
    "Forever and always, let our love bloom,",
    "In the garden of roses, amidst sweet perfume."


]

# Create lyric images as numpy arrays
lyric_images = []
for line in poem:
    lyric_image = create_lyric_image(line)
    lyric_images.append(np.array(lyric_image))  # Convert PIL Image to numpy array

# Create a video clip from images
video_clip = ImageSequenceClip(lyric_images, fps=1)  # Adjust FPS as needed

# Export the video
output_video_path = "/home/jasvir/Music/romantic_poem_video.mp4"
video_clip.write_videofile(output_video_path, codec='libx264')
