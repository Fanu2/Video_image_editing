import os
from PIL import Image
from moviepy.editor import ImageSequenceClip, AudioFileClip


def resize_image(image_path, target_size):
    """Resize an image to the target size."""
    with Image.open(image_path) as img:
        img_resized = img.resize(target_size, Image.LANCZOS)
        return img_resized


def create_video_from_images_and_sound(images_folder, sound_file, output_video, target_size=(1920, 1080)):
    # Get a list of image files
    image_files = sorted([os.path.join(images_folder, img) for img in os.listdir(images_folder) if
                          img.lower().endswith(('.png', '.jpg', '.jpeg'))])

    if not image_files:
        raise ValueError("No images found in the specified folder.")

    # Load the audio file
    if not os.path.isfile(sound_file):
        raise ValueError(f"The specified sound file does not exist: {sound_file}")

    audio_clip = AudioFileClip(sound_file)
    audio_duration = audio_clip.duration  # Duration of the audio in seconds

    # Calculate duration for each image
    num_images = len(image_files)
    if num_images == 0:
        raise ValueError("No images found in the specified folder.")

    duration_per_image = audio_duration / num_images

    # Resize images to the target size
    resized_images = []
    for img_path in image_files:
        resized_img = resize_image(img_path, target_size)
        temp_resized_path = img_path.replace('.jpg', '_resized.jpg').replace('.png', '_resized.png')
        resized_img.save(temp_resized_path, format='JPEG' if temp_resized_path.endswith('.jpg') else 'PNG')
        resized_images.append(temp_resized_path)

    # Create a video clip with specified duration per image
    video_clip = ImageSequenceClip(resized_images, durations=[duration_per_image] * num_images)

    # Set the audio of the video clip
    video_clip = video_clip.set_audio(audio_clip)

    # Write the video to file
    video_clip.write_videofile(output_video, codec='libx264', fps=24)

    # Clean up temporary resized images
    for img_path in resized_images:
        os.remove(img_path)

    print(f"Video saved as {output_video}")


if __name__ == "__main__":
    # Ask user for input
    images_folder = input("Enter the path to the folder with images: ")
    sound_file = input("Enter the path to the sound file (e.g., /path/to/sound.mp3): ")
    output_video = input("Enter the path where the video will be saved (e.g., /path/to/output_video.mp4): ")

    # Validate if input paths are correct
    if not os.path.isdir(images_folder):
        raise ValueError(f"The specified images folder does not exist: {images_folder}")

    if not os.path.isfile(sound_file):
        raise ValueError(f"The specified sound file does not exist: {sound_file}")

    if os.path.isdir(output_video):
        raise ValueError(
            f"The specified output path is a directory. Please provide a full file path for the output video: {output_video}")

    # Create the video
    create_video_from_images_and_sound(images_folder, sound_file, output_video, target_size=(1920, 1080))
