ffmpeg -i udp://127.0.0.1:1234 -c copy -f segment -segment_time 60 -reset_timestamps 1 output_%03d.mp4
