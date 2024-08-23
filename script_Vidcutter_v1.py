from moviepy.editor import VideoFileClip


def split_video(input_video, segment_length=60):
    # Load the video
    video = VideoFileClip(input_video)

    # Get the duration of the video in seconds
    duration = int(video.duration)

    # Split the video into segments
    segments = []
    for start_time in range(0, duration, segment_length):
        end_time = min(start_time + segment_length, duration)
        segment = video.subclip(start_time, end_time)
        segments.append(segment)

    # Save each segment to a new file
    for i, segment in enumerate(segments):
        output_path = f"{input_video[:-4]}_segment_{i + 1}.mp4"
        segment.write_videofile(output_path, codec="libx264", audio_codec="aac")
        print(f"Segment {i + 1} saved to {output_path}")


if __name__ == "__main__":
    input_video_path = "/media/jasvir/My Passport/media/mp4/a1.mp4"  # Your video path
    split_video(input_video_path)
