from moviepy.editor import VideoFileClip

def cut_first_60_seconds(input_video, output_video):
    # Load the video
    clip = VideoFileClip(input_video)

    # Cut the first 60 seconds
    short_clip = clip.subclip(0, 60)

    # Write the result to a file
    short_clip.write_videofile(output_video, codec="libx264", audio_codec="aac")

if __name__ == "__main__":
    input_video_path = "/home/jasvir/Videos/Waqat ne kiya .mp4"  # Your video path
    output_video_path = "/home/jasvir/Videos/Waqat ne kiya .mp4_first_60_seconds.mp4"  # Desired output path

    cut_first_60_seconds(input_video_path, output_video_path)
