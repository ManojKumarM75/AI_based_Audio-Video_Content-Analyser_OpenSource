# 20241109 Packet error and packet loss

import cv2
import numpy as np
import random

def simulate_network_artifacts(video_path):
    # Initialize video capture and writer
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # 1. Packet Loss Simulation
            # Creates complete black blocks simulating lost data packets
            if random.random() < 0.1:  # 10% chance of packet loss
                block_size = 16  # Standard macroblock size
                x = random.randint(0, frame.shape[1] - block_size)
                y = random.randint(0, frame.shape[0] - block_size)
                frame[y:y+block_size, x:x+block_size] = 0
            
            # 2. Packet Corruption Simulation
            # Creates noisy blocks representing corrupted data
            if random.random() < 0.05:  # 5% chance of corruption
                block_size = 32  # Larger block size for corruption
                x = random.randint(0, frame.shape[1] - block_size)
                y = random.randint(0, frame.shape[0] - block_size)
                # Generate random noise for corrupted blocks
                noise = np.random.randint(0, 255, (block_size, block_size, 3))
                frame[y:y+block_size, x:x+block_size] = noise
            
            # 3. Frame Freezing Simulation
            # Simulates buffer underrun by repeating frames
            if random.random() < 0.02:  # 2% chance of frame freeze
                frame = prev_frame.copy()
            
            # 4. Signal Interference Simulation
            # Adds Gaussian noise to simulate interference
            if random.random() < 0.03:  # 3% chance of interference
                # Generate and apply Gaussian noise
                noise = np.random.normal(0, 25, frame.shape)
                frame = np.clip(frame + noise, 0, 255).astype(np.uint8)
            
            # 5. Color Shift Simulation
            # Simulates signal degradation with color shifting
            if random.random() < 0.04:  # 4% chance of color shift
                # Randomly adjust color channels
                frame[:,:,random.randint(0,2)] = np.clip(
                    frame[:,:,random.randint(0,2)] * 1.5, 0, 255
                )
            
            # Store current frame for freeze effect
            prev_frame = frame.copy()
            # Write the modified frame
            out.write(frame)
            
    # Clean up resources
    cap.release()
    out.release()

# Usage example
if __name__ == "__main__":
    simulate_network_artifacts("input.mp4")
