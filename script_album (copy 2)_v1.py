from moviepy.editor import VideoFileClip, clips_array

# Paths to the video files
video_paths = [
    '/home/jasvir/Music/Movie work/5.mp4',
    '/home/jasvir/Music/Movie work/6.mp4',
    '/home/jasvir/Music/Movie work/4.mp4',
    '/home/jasvir/Music/Movie work/7.mp4'
]

# Duration for each clip in seconds
clip_duration = 20

# Load and trim video clips
clips = [VideoFileClip(video).subclip(0, clip_duration) for video in video_paths]

# Resize clips if needed to ensure they fit in the grid
clips = [clip.resize(height=360) for clip in clips]  # Adjust height and width as needed

# Create a 2x2 grid of the clips
final_clip = clips_array([[clips[0], clips[1]], [clips[2], clips[3]]])

# Write the result to a file
final_clip.write_videofile('/home/jasvir/Music/Movie work/output_video1.mp4', codec='libx264')

