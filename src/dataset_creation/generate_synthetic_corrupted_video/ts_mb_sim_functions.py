import random

def usage_example() -> None:
    print("\n\nUsage: \n")
    print("\tcmd  -> python ts_mb_sim [file.ts] [30] \n")
    print("\targ_1-> [file.ts] -> is .ts ? Required.\n")
    print("\targ_2-> [30] -> will be taken as 30 %. Required.\n\n")

def random_bytes(bt_len:int) -> list:
    random_bytes = bytes([random.randint(0, 255) for _ in range(bt_len-1)])
    hex_bytes = [hex(byte) for byte in random_bytes]
    return hex_bytes


def get_new(packet:bytes, change_prob:float, seg:int) -> bytes:
    if random.random() < change_prob: #probabity to change bytes or not
        bts = list(packet)
        hex_list = [hex(byte) for byte in bts]
        if seg == 0:
            start = random.randint(2, len(hex_list)) - 1   # Ensure start is less than stop
            stop = random.randint(2, len(hex_list)) + 1
        else:
            seg = (seg/100) * len(hex_list)
            start = random.randint(2, len(hex_list))
            stop = int(start + seg)
        selected = hex_list[start:stop]
        unselected_front = hex_list[:start]
        unselected_back = hex_list[stop:]
        byte_length = len(selected)
        new_bytes = random_bytes(byte_length)
        new_hex = unselected_front + new_bytes + unselected_back
        new_hex_bytes = bytes.fromhex(''.join(hex_value[2:].zfill(2) for hex_value in new_hex))
        return new_hex_bytes
    else:
        return packet

def get_packets(data:bytes) -> list:
    packet_size = 188
    packets = [bytes(data[i:i + packet_size]) for i in range(0, len(data), packet_size)]
    print("Length of packets in the file-",len(packets))
    return packets


def change_bytes(packets:list, change_prob:float=0.00001, seg_length:int=1) -> list:
    new_packets = []
    for packet in packets:
        n = get_new(packet, change_prob, seg_length)
        new_packets.append(n)
    return new_packets


def lose_packets(new_packets:list, loss_rate:float=0.0001) -> list:
    rc_packs = []
    count = 0
    idxs = []
    for index,packet in enumerate(new_packets):
        if random.random() >= loss_rate: 
            rc_packs.append(packet)
            count += 1
        else:
            idxs.append(index)
    print(f"{len(new_packets)-count} packets lost out of {len(new_packets)}")
    return rc_packs


def reorder_packets(t_packs:list, reorder_prob:float=0.001) -> list:
    vid_len = int(len(t_packs)/100)
    reorder_len = 200
    for i in range(1, vid_len):
        if random.random() < reorder_prob :
            _start = i*100
            _stop = (i*100) + reorder_len 
            t_packs[_start:_stop] = t_packs[_start:_stop][::-1]
    return t_packs


def read_file(filename:str="input.ts") -> bytes:
    if filename.split('.')[-1] != 'ts':
        usage_example()
        raise TypeError("Only .ts files are supported, you can covert mp4 to ts via ffmpeg.")
    else:
        with open(filename, 'rb') as f_in:
            data = f_in.read()
        return data
            

def write_file(packets, filename:str="output.ts") -> None:
    with open(filename, 'wb') as f_out:
        f_out.write(b''.join(packets))

def map_severity(severity:float) -> tuple:
    severity = severity/2
    _loss_rate = severity * 0.0001
    _change_prob = severity * 0.00001
    _reorder_prob = severity * 0.001
    _seg_length = severity/10
    return (_loss_rate, _change_prob, _reorder_prob, _seg_length)