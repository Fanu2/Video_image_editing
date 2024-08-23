from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

def add_frame(video_path, frame_image_path, output_path):
    video = VideoFileClip(video_path)
    frame = ImageClip(frame_image_path).set_duration(video.duration).set_position('center').resize(video.size)
    video_with_frame = CompositeVideoClip([video, frame])
    video_with_frame.write_videofile(output_path)

# Example usage
add_frame('input.mp4', 'frame.png', 'output_with_frame.mp4')
