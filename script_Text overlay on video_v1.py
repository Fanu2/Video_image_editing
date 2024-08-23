import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip

def overlay_text_on_concatenated_video(input_folder, text_to_overlay, position='bottom', fontsize=50):
    # Get all video files in the input folder (sorted by filename)
    video_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.mp4')])

    clips = []
    for file_name in video_files:
        file_path = os.path.join(input_folder, file_name)
        try:
            # Load video clip
            video_clip = VideoFileClip(file_path)
            clips.append(video_clip)
        except Exception as e:
            print(f"Failed to process {file_name}: {e}")

    if len(clips) == 0:
        print("No valid videos found in the input folder.")
        return

    # Concatenate video clips
    final_clip = concatenate_videoclips(clips)

    # Overlay text on final_clip
    txt_clip = TextClip(text_to_overlay, fontsize=fontsize, color='white', bg_color='black', size=(final_clip.w, None), method='caption', align='center', font='Arial')
    if position == 'bottom':
        txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(final_clip.duration)
    elif position == 'top':
        txt_clip = txt_clip.set_position(('center', 'top')).set_duration(final_clip.duration)
    else:
        print(f"Unsupported position '{position}', using 'bottom' instead.")
        txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(final_clip.duration)

    # Composite the text clip onto the video
    final_clip = final_clip.set_audio(None)  # Remove audio from concatenated video (optional)
    final_clip = final_clip.set_duration(txt_clip.duration)

    final_clip = final_clip.set_audio(None).set_fps(24)

    # Write the final video with text overlay
    output_video = os.path.join(input_folder, 'output_video.mp4')
    final_clip.write_videofile(output_video, codec='libx264', fps=24)

if __name__ == "__main__":
    input_folder = '/home/jasvir/Music/Jodha1/'
    text_to_overlay = "Text to overlay"

    overlay_text_on_concatenated_video(input_folder, text_to_overlay)
