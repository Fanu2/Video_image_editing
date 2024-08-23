import os
import warnings
from odf.opendocument import load
from odf.text import P
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip

# Suppress specific warnings
warnings.filterwarnings('ignore', message='In the future version we will turn default option ignore_ncx to True.')


def extract_text_from_odt(odt_path):
    """Extracts and returns text content from an ODT file, preserving poem structure."""
    doc = load(odt_path)
    text = ""
    for p in doc.getElementsByType(P):
        item_text = ''.join(node.data for node in p.childNodes if hasattr(node, 'data'))
        if item_text.strip():
            text += item_text + "\n\n"
    if not text.strip():
        raise ValueError("Extracted text is empty.")
    return text


def create_images_from_text(text, output_folder, img_width=1280, img_height=720, font_size=30, margin=50,
                            bg_color=(255, 255, 255), text_color=(0, 0, 0)):
    """Creates images from text with poem formatting and saves them in the output folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Use DejaVu Sans font available in most Linux distributions
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
    if not os.path.isfile(font_path):
        raise FileNotFoundError(f"Font file not found: {font_path}")

    font = ImageFont.truetype(font_path, font_size)
    lines = text.split('\n')

    images = []
    img = Image.new('RGB', (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(img)
    y = margin
    img_number = 0

    for line in lines:
        if y + font_size > img_height - margin:
            img_path = os.path.join(output_folder, f"img_{img_number:04d}.png")
            img.save(img_path)
            images.append(img_path)
            print(f"Saved image: {img_path}")  # Debug print
            img = Image.new('RGB', (img_width, img_height), bg_color)
            draw = ImageDraw.Draw(img)
            y = margin
            img_number += 1
        draw.text((margin, y), line, font=font, fill=text_color)
        y += font_size + 10  # Added spacing between lines

    # Save the last image
    img_path = os.path.join(output_folder, f"img_{img_number:04d}.png")
    img.save(img_path)
    images.append(img_path)
    print(f"Saved image: {img_path}")  # Debug print

    return images


def create_video_from_images(images, video_path, fps=1):
    """Creates a video from a list of images."""
    if not images:
        raise ValueError("No images to create video.")
    print(f"Creating video from {len(images)} images.")  # Debug print
    clip = ImageSequenceClip(images, fps=fps)
    clip.write_videofile(video_path, codec='libx264')
    print(f"Video created successfully at: {video_path}")  # Debug print


def main():
    odt_path = '/home/jasvir/Music/Movie work/Epub/Collection of Poems.odt'
    output_folder = '/home/jasvir/Music/Movie work/Epub/frames/'
    video_path = '/home/jasvir/Music/Movie work/Epub/Collection_of_Poems1.mp4'

    try:
        text = extract_text_from_odt(odt_path)
        if not text.strip():
            raise ValueError("Extracted text is empty.")
        print(f"Extracted {len(text.split())} words from ODT.")  # Debug print
        images = create_images_from_text(text, output_folder)
        create_video_from_images(images, video_path)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
