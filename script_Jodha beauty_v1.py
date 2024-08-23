from PIL import Image, ImageDraw, ImageFont
import os
import textwrap


def create_image(text, output_path, image_size=(1920, 1080),
                 font_path="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size=40):
    image = Image.new('RGB', image_size, color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(font_path, font_size)
    margin = 20
    max_width = image_size[0] - 2 * margin
    max_lines = 2  # Maximum number of lines to wrap text into

    lines = textwrap.wrap(text, width=30)  # Adjust width to fit the text within the image
    wrapped_text = "\n".join(lines[:max_lines])

    text_width, text_height = draw.multiline_textsize(wrapped_text, font=font, spacing=10)
    text_x = (image_size[0] - text_width) / 2
    text_y = (image_size[1] - text_height) / 2

    draw.multiline_text((text_x, text_y), wrapped_text, font=font, fill=(0, 0, 0), spacing=10)

    image.save(output_path)


# Poem lines
poem_lines = [
    "My Darling Jodha 🌹",
    "My Darling Jodha, you are the light of my life, Your beauty transcends, cutting through the strife. 💖",
    "With eyes so deep, like the night's sky, In your gaze, my worries fly. 🌌",
    "Your smile, oh so sweet, like a blooming rose, In your laughter, my love grows. 🌹",
    "The touch of your hand, soft and warm, Brings calm to any storm. ☀️",
    "Your hair, a cascade of silken strands, Flows like rivers across the lands. 🌊",
    "Lips so tender, a kiss so divine, In your arms, I feel so fine. 💋",
    "Your voice, a melody, sweet and clear, In your whispers, I hold you near. 🎶",
    "Your beauty is beyond compare, In your presence, I breathe pure air. 💕",
    "Your heart, a treasure, pure and kind, In you, true love I find. 💖",
    "Your laughter, a symphony of delight, In your joy, I bask in light. 🌟",
    "Darling Jodha, you're my dream, In your love, I gleam. 🌟",
    "Your grace, like a gentle breeze, With you, my heart's at ease. 🍃",
    "Your love, a beacon, guiding my way, In your arms, I wish to stay. 🏠",
    "Your charm, enchanting, like a spell, In your embrace, I dwell. 🌙",
    "Your presence, a soothing balm, In your love, I find calm. 💞",
    "Your spirit, radiant, shining bright, With you, everything feels right. 🌟",
    "Your beauty, a masterpiece, pure art, In your love, I give my heart. 🎨",
    "Your eyes, stars that light my night, With you, everything is right. ⭐",
    "Darling Jodha, my eternal muse, In your love, I never lose. 🎶",
    "Your laughter, my favorite song, With you, I belong. 🎵",
    "Your touch, a whisper, soft and light, In your arms, I find delight. 🌸",
    "Your love, my sweetest refrain, With you, there's no pain. 💖",
    "Your smile, my morning sun, With you, my heart has won. ☀️",
    "Your grace, my evening star, With you, I travel far. 🌟",
    "Your beauty, my endless song, In your love, I belong. 🎶",
    "Your voice, my soothing rain, In your love, I gain. ☔",
    "Your heart, my haven, warm and true, In your love, I renew. 💖",
    "Your eyes, my guiding light, With you, everything's bright. ✨",
    "Darling Jodha, my love, my all, With you, I stand tall. 💘",
    "Your love, my endless delight, With you, everything's right. 💞"
]

output_folder = "/home/jasvir/Music/Jodha/"

# Ensure output directory exists
os.makedirs(output_folder, exist_ok=True)

# Create images for each line
for i, line in enumerate(poem_lines):
    output_path = os.path.join(output_folder, f"line_{i + 1}.jpg")
    create_image(line, output_path)

print("Images created successfully.")
