import sys
from ts_mb_sim_functions import read_file, write_file, change_bytes, reorder_packets, lose_packets, get_packets, usage_example, map_severity

def process_file(input_file:str, severity:float) -> None:
    _loss_rate, _change_prob, _reorder_prob, _seg_length = map_severity(severity)
    data = read_file(input_file)
    packets = get_packets(data)
    packets = lose_packets(packets,loss_rate=_loss_rate)
    packets = change_bytes(packets, change_prob=_change_prob, seg_length=_seg_length)
    packets = reorder_packets(packets, reorder_prob=_reorder_prob)
    write_file(packets)

if len(sys.argv) > 2:
    process_file(sys.argv[1] , float(sys.argv[2]))
else:
    usage_example()
    raise ValueError("Please provide an input file & severity in %.")



