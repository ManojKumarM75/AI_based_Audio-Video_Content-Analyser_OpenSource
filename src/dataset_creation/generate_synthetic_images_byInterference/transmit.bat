ffmpeg -re -i input_video.mp4 -c:v libx264 -preset ultrafast -tune zerolatency -f mpegts udp://127.0.0.1:1234
