from moviepy.editor import VideoFileClip

def video_to_audio(video_path, output_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(output_path)

# Example usage
video_to_audio('input.mp4', 'output_audio.mp3')
