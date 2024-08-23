from moviepy.editor import VideoFileClip


def convert_to_shorts(input_video, output_video):
    # Load the video
    clip = VideoFileClip(input_video)

    # Cut the first 60 seconds
    short_clip = clip.subclip(0, 60)

    # Convert to vertical format (mobile mode)
    # Assuming 9:16 aspect ratio for YouTube Shorts
    w, h = short_clip.size
    target_aspect_ratio = 9 / 16
    target_width = h * target_aspect_ratio

    if w > target_width:
        # Crop the sides to fit the aspect ratio
        x_center = w / 2
        x1 = x_center - target_width / 2
        x2 = x_center + target_width / 2
        short_clip = short_clip.crop(x1=x1, x2=x2)
    else:
        # Pad the top and bottom if needed (unlikely for horizontal to vertical conversion)
        target_height = w / target_aspect_ratio
        y_center = h / 2
        y1 = y_center - target_height / 2
        y2 = y_center + target_height / 2
        short_clip = short_clip.crop(y1=y1, y2=y2)

    # Resize to common mobile resolution (1080x1920)
    short_clip = short_clip.resize(height=1920)

    # Write the result to a file
    short_clip.write_videofile(output_video, codec="libx264", audio_codec="aac")


if __name__ == "__main__":
    input_video_path = "/media/jasvir/My Passport/media/mp4/a1.mp4"  # Your video path
    output_video_path = "/home/jasvir/Documents/a1.mp4"  # Desired output path

    convert_to_shorts(input_video_path, output_video_path)
