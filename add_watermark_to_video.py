from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

def add_watermark(video_path, watermark_path, output_path):
    video = VideoFileClip(video_path)
    watermark = ImageClip(watermark_path).set_duration(video.duration).set_position(('right', 'bottom'))
    video_with_watermark = CompositeVideoClip([video, watermark])
    video_with_watermark.write_videofile(output_path)

# Example usage
add_watermark('input.mp4', 'watermark.png', 'output_watermarked.mp4')
