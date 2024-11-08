#20241101 MKM - not tested.
'''
Key severity controls:
  packet_loss_rate: Controls percentage of affected packets
  sync_loss_rate: Controls how often sync bytes get corrupted
  burst_mode: Enables consecutive packet corruption
  burst_length: Controls length of error bursts

Usage examples:
  python ts_severity_corruptor.py

The script creates three files with different interference levels:

  light_corrupt.ts: Occasional glitches
  medium_corrupt.ts: Noticeable interference
  heavy_corrupt.ts: Severe signal problems
You can fine-tune these parameters to match any real-world scenario from minor signal issues to major transmission problems.
'''
import random
import sys

def corrupt_ts_file(input_file, output_file, 
                   packet_loss_rate=0.05,    # % of packets affected
                   sync_loss_rate=0.2,       # % of corrupted packets that lose sync
                   burst_mode=False,         # Enable burst errors
                   burst_length=5):          # Number of consecutive packets in burst
    
    with open(input_file, 'rb') as f_in:
        data = f_in.read()
    
    packet_size = 188
    packets = [data[i:i+packet_size] for i in range(0, len(data), packet_size)]
    
    corrupted_packets = []
    in_burst = False
    burst_count = 0
    
    for packet in packets:
        should_corrupt = random.random() < packet_loss_rate
        
        if burst_mode:
            if should_corrupt and not in_burst:
                in_burst = True
                burst_count = 0
            if in_burst:
                should_corrupt = True
                burst_count += 1
                if burst_count >= burst_length:
                    in_burst = False
        
        if should_corrupt:
            if random.random() < sync_loss_rate:
                # Total corruption including sync byte
                corrupted_packet = bytes([random.randint(0, 255) for _ in range(188)])
            else:
                # Corruption preserving sync byte
                corrupted_packet = b'\x47' + bytes([random.randint(0, 255) for _ in range(187)])
            corrupted_packets.append(corrupted_packet)
        else:
            corrupted_packets.append(packet)
    
    with open(output_file, 'wb') as f_out:
        f_out.write(b''.join(corrupted_packets))

# Example usage with different severity levels
def main():
    # Light interference
    corrupt_ts_file('input.ts', 'light_corrupt.ts', 
                   packet_loss_rate=0.01, 
                   sync_loss_rate=0.1)
    
    # Medium interference
    corrupt_ts_file('input.ts', 'medium_corrupt.ts', 
                   packet_loss_rate=0.05, 
                   sync_loss_rate=0.2,
                   burst_mode=True,
                   burst_length=3)
    
    # Heavy interference
    corrupt_ts_file('input.ts', 'heavy_corrupt.ts', 
                   packet_loss_rate=0.15, 
                   sync_loss_rate=0.4,
                   burst_mode=True,
                   burst_length=8)

if __name__ == '__main__':
    main()
