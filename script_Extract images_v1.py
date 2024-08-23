import cv2
import os

def extract_images(video_path, output_folder, frame_rate=1):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    video_capture = cv2.VideoCapture(video_path)

    # Get the total number of frames in the video
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the interval between frames to capture based on the frame rate
    interval = int(video_capture.get(cv2.CAP_PROP_FPS) / frame_rate)

    frame_number = 0
    saved_frame_number = 0

    while True:
        # Read the next frame from the video
        success, frame = video_capture.read()

        if not success:
            break

        # Save the frame if it is at the desired interval
        if frame_number % interval == 0:
            frame_filename = os.path.join(output_folder, f"frame_{saved_frame_number:05d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_frame_number += 1

        frame_number += 1

    # Release the video capture object
    video_capture.release()

    print(f"Extracted {saved_frame_number} frames from the video.")

# Example usage
video_path = '/home/jasvir/Music/Movie work/studio/download.mp4'
output_folder = '/home/jasvir/Music/Movie work/studio/'
frame_rate = 1  # Extract one frame per second

extract_images(video_path, output_folder, frame_rate)
