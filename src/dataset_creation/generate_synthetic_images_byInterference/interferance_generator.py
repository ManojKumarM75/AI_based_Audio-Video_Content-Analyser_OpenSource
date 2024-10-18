import subprocess
import time
import random

CLUMSY_PATH = r"C:\Path\To\clumsy.exe"

def set_packet_loss(loss_percentage):
    subprocess.run([CLUMSY_PATH, "--filter", f"outbound and udp", "--drop", f"--chance {loss_percentage}"])

def main():
    while True:
        # Random packet loss between 1% and 10%
        loss = random.uniform(1, 10)
        set_packet_loss(loss)
        print(f"Set packet loss to {loss}%")
        
        # Wait for a random time between 5 and 15 seconds before changing again
        time.sleep(random.uniform(5, 15))

if __name__ == "__main__":
    main()
