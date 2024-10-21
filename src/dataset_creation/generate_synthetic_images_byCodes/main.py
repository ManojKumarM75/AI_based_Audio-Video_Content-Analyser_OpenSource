from configurations import DEMO_CONFIG
import os
import glob
from tqdm import tqdm
from datagen import process_extracted_frames

#extract the frames

video_directory = DEMO_CONFIG['input']
output_directory = DEMO_CONFIG['frames']
fps = DEMO_CONFIG['fps']

os.makedirs(output_directory, exist_ok=True)

# Get a list of all video files in the directory
video_files = glob.glob(os.path.join(video_directory, '*.mp4'))  # Adjust the extension as needed

num_videos = len(video_files)
print(f'Found {num_videos} video(s) in the directory.')

for video_file in tqdm(video_files, desc='Extracting frames', unit='video'):
    # Get the base name of the video file (without the directory)
    base_name = os.path.basename(video_file)
    fileName = os.path.splitext(base_name)[0]
    video_output_directory = output_directory
    #video_output_directory = os.path.join(output_directory, os.path.splitext(base_name)[0])
    os.makedirs(video_output_directory, exist_ok=True)

    # Construct the ffmpeg command
    command = f'ffmpeg -i "{video_file}" -vf "fps={fps}" "{video_output_directory}/{fileName}_%04d.jpg"'
    os.system(command)

print('Frame extraction completed.')


# Process extracted frames

extracted_frames_folder = DEMO_CONFIG['frames']  # Output folder for extracted frames
modified_frames_folder = DEMO_CONFIG['mod_frames']  # Output folder for modified frames
base_parameters = DEMO_CONFIG['params'] # Base parameters for randomization
num_variations = DEMO_CONFIG['variations'] # Number of variations to apply to each frame

process_extracted_frames(extracted_frames_folder, modified_frames_folder, base_parameters, num_variations)
