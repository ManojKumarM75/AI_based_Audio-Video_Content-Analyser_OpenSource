To simulate network packet loss and test video transmission with interference on a Windows laptop, you can use a combination of tools and scripts. Here's a step-by-step approach to achieve what you're looking for:

Video Transmission: Use FFmpeg to stream the video over UDP. FFmpeg is a powerful tool for video processing and streaming.

Network Packet Loss Simulation: Use Clumsy, a tool for Windows that can simulate network conditions including packet loss.

Video Reception and Saving: Use FFmpeg again to receive the stream and save it in chunks.

Interference Generator: Create a Python script to control Clumsy dynamically, simulating varying levels of interference.

Here's how you can set this up:

Install required tools:

FFmpeg: https://ffmpeg.org/download.html
Clumsy: https://jagt.github.io/clumsy/
Python: https://www.python.org/downloads/

Run the simulation:
a. Start Clumsy 
b. Run the interference_generator.py script 
c. Run the receive.bat script 
d. Run the transmit.bat script

This setup will:

Transmit the video over UDP
Simulate packet loss using Clumsy, controlled by the Python script
Receive and save the video in 1-minute chunks
The received video will show macroblock artifacts due to the simulated packet loss. The interference levels will change randomly over time, causing varying degrees of artifacts in the received video.

Note:

This setup uses localhost (127.0.0.1) for simplicity. You can modify the IP addresses if you want to test between different machines.
Adjust the packet loss range in the Python script to simulate different levels of interference.
Make sure to replace the paths in the scripts with the correct paths on your system.
This setup provides a basic framework for your experiment. You may need to fine-tune parameters like video encoding settings, packet loss ranges, or timing to achieve the specific results you're looking for.