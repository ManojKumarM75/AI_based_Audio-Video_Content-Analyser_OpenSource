import subprocess
import pydivert
import random
import time
import threading

def transmit_stream(input_file, target_ip, target_port):
    """Start FFmpeg to transmit a video stream"""
    command = [
        "ffmpeg",
        "-re",
        "-i", input_file,
        "-f", "rtp",
        f"rtp://{target_ip}:{target_port}"
    ]
    subprocess.Popen(command)

def launch_vlc(receive_port):
    """Launch VLC to receive a stream"""
    command = [
        "vlc",
        f"rtp://@:{receive_port}"
    ]
    subprocess.Popen(command)

def simulate_packet_loss(interface="eth0", loss_percentage=5, delay_ms=100):
    """Simulate packet loss and delay using PyDivert"""
    filter_expression = "outbound and tcp.DstPort == 5004"
    with pydivert.WinDivert(filter_expression) as w:
        for packet in w:
            if random.randint(1, 100) <= loss_percentage:
                print("Packet dropped")
                continue  # Drop the packet
            time.sleep(delay_ms / 1000.0)
            w.send(packet)

# Example usage
if __name__ == "__main__":
    # Step 1: Start streaming with FFmpeg
    threading.Thread(target=transmit_stream, args=("input.mp4", "192.168.1.100", 5004)).start()

    # Step 2: Start VLC to receive the stream
    threading.Thread(target=launch_vlc, args=(5004,)).start()

    # Step 3: Simulate network issues with PyDivert
    simulate_packet_loss(loss_percentage=10, delay_ms=50)
