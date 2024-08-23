from moviepy.editor import VideoFileClip

def change_aspect_ratio(video_path, output_path, new_aspect_ratio):
    video = VideoFileClip(video_path)
    new_size = (int(video.size[1] * new_aspect_ratio), video.size[1])
    resized_video = video.resize(new_size)
    resized_video.write_videofile(output_path)

# Example usage
change_aspect_ratio('input.mp4', 'output_aspect_ratio.mp4', 16/9)
