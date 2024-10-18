import subprocess
import random

def generate_artifacts(input_file, output_file, artifact_intensity=0.1, duration=None):
    # Base FFmpeg command
    command = ['ffmpeg', '-i', input_file]

    # Add duration parameter if specified
    if duration:
        command.extend(['-t', str(duration)])

    # Add filters to create artifacts
    filters = []

    # Macro blocking effect
    block_size = random.randint(16, 64)
    filters.append(f"select='not(mod(n,{int(1/artifact_intensity)}))',geq='if(mod(X,{block_size})+mod(Y,{block_size})==0,255,p(X,Y))'")

    # Color shift effect
    color_shift = random.uniform(0.95, 1.05)
    filters.append(f"colorchannelmixer=rr={color_shift}:gg={color_shift}:bb={color_shift}")

    # Occasional frame drop (simulating packet loss)
    filters.append(f"select='not(mod(n,{int(1/(artifact_intensity*0.1))}))'")

    # Blank frames (simulating encoder behavior for packet loss)
    blank_frame_freq = int(1 / (artifact_intensity * 0.05))
    filters.append(f"select='if(not(mod(n,{blank_frame_freq})),0,1)',drawbox=c=black@1:t=fill")

    # Freeze frames
    freeze_duration = random.randint(2, 5)
    freeze_freq = int(1 / (artifact_intensity * 0.02))
    filters.append(f"freeze=duration={freeze_duration}:n={freeze_freq}")

    # Apply filters
    command.extend(['-vf', ','.join(filters)])

    # Output settings (Constant Bitrate encoding)
    target_bitrate = '5M'  # Adjust as needed
    command.extend(['-c:v', 'libx264', '-b:v', target_bitrate, '-minrate', target_bitrate, '-maxrate', target_bitrate, '-bufsize', '1M', output_file])

    # Run FFmpeg command
    subprocess.run(command, check=True)

# Example usage
input_video = 'input.mp4'
output_video = 'output_with_artifacts.mp4'
generate_artifacts(input_video, output_video, artifact_intensity=0.05, duration=10)