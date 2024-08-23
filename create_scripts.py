import os

project_path = '/home/jasvir/PycharmProjects/Top50AutomationScripts/scripts/'

additional_scripts = {
    'rotate_image.py': """\
from PIL import Image

def rotate_image(input_path, output_path, angle):
    with Image.open(input_path) as img:
        rotated_img = img.rotate(angle, expand=True)
        rotated_img.save(output_path)

# Example usage
rotate_image('input.jpg', 'output_rotated.jpg', 45)
""",
    'crop_video.py': """\
from moviepy.editor import VideoFileClip

def crop_video(input_path, output_path, crop_area):
    video = VideoFileClip(input_path)
    cropped_video = video.crop(x1=crop_area[0], y1=crop_area[1], x2=crop_area[2], y2=crop_area[3])
    cropped_video.write_videofile(output_path)

# Example usage
crop_video('input.mp4', 'output_cropped.mp4', (100, 100, 500, 500))
""",
    'add_text_overlay.py': """\
from PIL import Image, ImageDraw, ImageFont

def add_text_overlay(input_path, output_path, text, position, font_size):
    with Image.open(input_path) as img:
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", font_size)
        draw.text(position, text, font=font, fill='white')
        img.save(output_path)

# Example usage
add_text_overlay('input.jpg', 'output_with_text.jpg', 'Hello!', (10, 10), 50)
""",
    'create_gif_from_video.py': """\
from moviepy.editor import VideoFileClip

def create_gif_from_video(video_path, output_path, start_time, end_time):
    video = VideoFileClip(video_path).subclip(start_time, end_time)
    video.write_gif(output_path)

# Example usage
create_gif_from_video('input.mp4', 'output.gif', 10, 20)
""",
    'add_subtitle_to_video.py': """\
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def add_subtitle(video_path, subtitle_text, output_path):
    video = VideoFileClip(video_path)
    subtitle = TextClip(subtitle_text, fontsize=24, color='white', bg_color='black', size=video.size)
    subtitle = subtitle.set_position(('center', 'bottom')).set_duration(video.duration)
    video_with_subtitle = CompositeVideoClip([video, subtitle])
    video_with_subtitle.write_videofile(output_path)

# Example usage
add_subtitle('input.mp4', 'This is a subtitle', 'output_with_subtitle.mp4')
""",
    'apply_gaussian_blur_to_video.py': """\
from moviepy.editor import VideoFileClip
from moviepy.video.fx import gaussian_blur

def apply_gaussian_blur_to_video(input_path, output_path, radius):
    video = VideoFileClip(input_path)
    blurred_video = gaussian_blur(video, radius)
    blurred_video.write_videofile(output_path)

# Example usage
apply_gaussian_blur_to_video('input.mp4', 'output_blurred.mp4', 5)
""",
    'extract_audio_from_video.py': """\
from moviepy.editor import VideoFileClip

def extract_audio(video_path, output_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(output_path)

# Example usage
extract_audio('input.mp4', 'output_audio.mp3')
""",
    'resize_image.py': """\
from PIL import Image

def resize_image(input_path, output_path, size):
    with Image.open(input_path) as img:
        resized_img = img.resize(size)
        resized_img.save(output_path)

# Example usage
resize_image('input.jpg', 'output_resized.jpg', (800, 600))
""",
    'convert_image_to_grayscale.py': """\
from PIL import Image

def convert_to_grayscale(input_path, output_path):
    with Image.open(input_path) as img:
        grayscale_img = img.convert('L')
        grayscale_img.save(output_path)

# Example usage
convert_to_grayscale('input.jpg', 'output_grayscale.jpg')
""",
    'generate_video_thumbnail.py': """\
from moviepy.editor import VideoFileClip

def generate_thumbnail(video_path, output_path, time):
    video = VideoFileClip(video_path)
    frame = video.get_frame(time)
    from PIL import Image
    Image.fromarray(frame).save(output_path)

# Example usage
generate_thumbnail('input.mp4', 'thumbnail.jpg', 5)
""",
    'add_transition_between_videos.py': """\
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx import fadein, fadeout

def add_transition(videos, output_path, transition_duration):
    clips = [fadein(fadeout(VideoFileClip(vid), transition_duration), transition_duration) for vid in videos]
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(output_path)

# Example usage
add_transition(['video1.mp4', 'video2.mp4'], 'output_with_transition.mp4', 1)
""",
    'overlay_text_on_video.py': """\
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def overlay_text_on_video(video_path, text, output_path):
    video = VideoFileClip(video_path)
    text_clip = TextClip(text, fontsize=24, color='white', bg_color='black', size=video.size)
    text_clip = text_clip.set_position(('center', 'bottom')).set_duration(video.duration)
    video_with_text = CompositeVideoClip([video, text_clip])
    video_with_text.write_videofile(output_path)

# Example usage
overlay_text_on_video('input.mp4', 'Overlay Text', 'output_with_text.mp4')
""",
    'extract_frames_at_interval.py': """\
from moviepy.editor import VideoFileClip
from PIL import Image

def extract_frames_at_interval(video_path, output_folder, interval):
    video = VideoFileClip(video_path)
    for t in range(0, int(video.duration), interval):
        frame = video.get_frame(t)
        Image.fromarray(frame).save(f"{output_folder}/frame_{t}.png")

# Example usage
extract_frames_at_interval('input.mp4', 'frames/', 10)
""",
    'add_background_music_to_slideshow.py': """\
from moviepy.editor import ImageSequenceClip, AudioFileClip, CompositeVideoClip

def add_background_music_to_slideshow(image_folder, audio_path, output_path, fps):
    import os
    images = [os.path.join(image_folder, img) for img in sorted(os.listdir(image_folder))]
    slideshow = ImageSequenceClip(images, fps=fps)
    audio = AudioFileClip(audio_path)
    video_with_music = slideshow.set_audio(audio)
    video_with_music.write_videofile(output_path)

# Example usage
add_background_music_to_slideshow('images/', 'background.mp3', 'slideshow_with_music.mp4', 1)
""",
    'convert_video_frames_to_images.py': """\
from moviepy.editor import VideoFileClip
from PIL import Image

def convert_frames_to_images(video_path, output_folder):
    video = VideoFileClip(video_path)
    for i, frame in enumerate(video.iter_frames()):
        img = Image.fromarray(frame)
        img.save(f"{output_folder}/frame_{i:04d}.png")

# Example usage
convert_frames_to_images('input.mp4', 'images/')
""",
    'add_logo_watermark_to_image.py': """\
from PIL import Image

def add_logo_watermark(image_path, logo_path, output_path, position):
    with Image.open(image_path) as img:
        with Image.open(logo_path) as logo:
            img.paste(logo, position, logo)
            img.save(output_path)

# Example usage
add_logo_watermark('input.jpg', 'logo.png', 'output_with_logo.jpg', (0, 0))
""",
    'apply_sepia_filter_to_image.py': """\
from PIL import Image, ImageOps

def apply_sepia_filter(input_path, output_path):
    with Image.open(input_path) as img:
        sepia_img = ImageOps.colorize(img.convert('L'), '#704214', '#C0C0C0')
        sepia_img.save(output_path)

# Example usage
apply_sepia_filter('input.jpg', 'output_sepia.jpg')
""",
    'split_video_into_clips.py': """\
from moviepy.editor import VideoFileClip

def split_video_into_clips(video_path, clip_duration, output_folder):
    video = VideoFileClip(video_path)
    duration = int(video.duration)
    for start_time in range(0, duration, clip_duration):
        end_time = min(start_time + clip_duration, duration)
        clip = video.subclip(start_time, end_time)
        clip.write_videofile(f"{output_folder}/clip_{start_time}.mp4")

# Example usage
split_video_into_clips('input.mp4', 10, 'clips/')
""",
    'create_collage_from_images.py': """\
from PIL import Image

def create_collage(image_paths, collage_path, size):
    images = [Image.open(img).resize(size) for img in image_paths]
    collage = Image.new('RGB', (size[0] * len(images), size[1]))
    for i, img in enumerate(images):
        collage.paste(img, (i * size[0], 0))
    collage.save(collage_path)

# Example usage
create_collage(['img1.jpg', 'img2.jpg'], 'collage.jpg', (300, 200))
""",
    'apply_contrast_enhancement.py': """\
from PIL import Image, ImageEnhance

def apply_contrast(input_path, output_path, factor):
    with Image.open(input_path) as img:
        enhancer = ImageEnhance.Contrast(img)
        img_enhanced = enhancer.enhance(factor)
        img_enhanced.save(output_path)

# Example usage
apply_contrast('input.jpg', 'output_contrast.jpg', 2)
"""
}

# Create the scripts in the project directory
for filename, content in additional_scripts.items():
    with open(os.path.join(project_path, filename), 'w') as file:
        file.write(content)

print("Additional scripts have been added.")
