import subprocess

import cv2

# RTMP服务器地址
rtmp = r'rtmp://127.0.0.1:33308/stream/car'
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
size = '1280x960'
cmd = ['ffmpeg',
       '-y', '-an',
       '-f', 'rawvideo',
       '-vcodec', 'rawvideo',
       '-pix_fmt', 'bgr24',
       '-s', size,
       '-r', '25',
       '-i', '-',
       '-c:v', 'libx264',
       '-pix_fmt', 'yuv420p',
       '-preset', 'ultrafast',
       '-f', 'flv',
       rtmp]
pipe = subprocess.Popen(cmd, shell=False, stdin=subprocess.PIPE)
while cap.isOpened():
    success, frame = cap.read()
    img_left = frame[0:960, 0:1280]
    if success:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        pipe.stdin.write(img_left.tostring())
cap.release()
pipe.terminate()
