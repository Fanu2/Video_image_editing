from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip

def add_music_to_video(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    video_with_audio = video.set_audio(audio)
    video_with_audio.write_videofile(output_path)

# Example usage
add_music_to_video('input.mp4', 'background_music.mp3', 'output_with_music.mp4')
