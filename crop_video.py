from moviepy.editor import VideoFileClip

def crop_video(input_path, output_path, crop_rect):
    video = VideoFileClip(input_path)
    video_cropped = video.crop(x1=crop_rect[0], y1=crop_rect[1], x2=crop_rect[2], y2=crop_rect[3])
    video_cropped.write_videofile(output_path)

# Example usage
crop_video('input.mp4', 'output_cropped.mp4', (100, 100, 500, 500))
