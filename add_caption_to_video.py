from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def add_caption(video_path, output_path, text, position, font_size):
    video = VideoFileClip(video_path)
    caption = TextClip(text, fontsize=font_size, color='white').set_duration(video.duration).set_position(position)
    video_with_caption = CompositeVideoClip([video, caption])
    video_with_caption.write_videofile(output_path)

# Example usage
add_caption('input.mp4', 'output_caption.mp4', 'Sample Caption', ('center', 'bottom'), 24)
