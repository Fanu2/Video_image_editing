from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def add_text_overlay(video_path, text, output_path):
    video = VideoFileClip(video_path)
    txt_clip = TextClip(text, fontsize=70, color='white')
    txt_clip = txt_clip.set_position('center').set_duration(video.duration)
    video_with_text = CompositeVideoClip([video, txt_clip])
    video_with_text.write_videofile(output_path)

# Example usage
add_text_overlay('input.mp4', 'Sample Text', 'output_with_text.mp4')
