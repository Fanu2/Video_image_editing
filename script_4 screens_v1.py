from moviepy.editor import VideoFileClip, clips_array


def main():
    # Path to the input video
    input_video_path = '/home/jasvir/Music/Movie work/Split screen/1.mp4'

    # Load the video
    video = VideoFileClip(input_video_path)

    # Get the duration of the video and calculate the duration of each part
    video_duration = video.duration
    part_duration = video_duration / 4

    # Split the video into 4 equal parts
    part1 = video.subclip(0, part_duration)
    part2 = video.subclip(part_duration, 2 * part_duration)
    part3 = video.subclip(2 * part_duration, 3 * part_duration)
    part4 = video.subclip(3 * part_duration, video_duration)

    # Resize the clips to fit in a 2x2 grid (assuming the original video is in landscape mode)
    part1_resized = part1.resize((video.size[0] // 2, video.size[1] // 2))
    part2_resized = part2.resize((video.size[0] // 2, video.size[1] // 2))
    part3_resized = part3.resize((video.size[0] // 2, video.size[1] // 2))
    part4_resized = part4.resize((video.size[0] // 2, video.size[1] // 2))

    # Create a split-screen video (2x2 grid)
    split_screen_video = clips_array([[part1_resized, part2_resized],
                                      [part3_resized, part4_resized]])

    # Limit the duration of the output video to 60 seconds
    split_screen_video = split_screen_video.subclip(0, 60)

    # Output path
    output_path = '/home/jasvir/Music/Movie work/Split screen/output_split_screen.mp4'

    # Write the output video to a file
    split_screen_video.write_videofile(output_path, codec='libx264')

    print(f"Split-screen video saved to {output_path}")


if __name__ == "__main__":
    main()
