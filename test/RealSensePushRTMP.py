## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################
import subprocess

import cv2
import numpy as np
import pyrealsense2 as rs

# RTMP服务器地址
rtmp = r'rtmp://127.0.0.1:33308/stream/car'

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)

# Start streaming
pipeline.start(config)


def get_coordinate(x, y):
    distance = depth_frame.get_distance(int(x), int(y))
    intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics
    coordinate = rs.rs2_deproject_pixel_to_point(intrinsics, [x, y], distance)
    return coordinate

size = '640x480'
cmd = ['ffmpeg',
       '-y', '-an',
       '-f', 'rawvideo',
       '-vcodec', 'rawvideo',
       '-pix_fmt', 'bgr24',
       '-s', size,
       '-r', '60',
       '-i', '-',
       '-c:v', 'libx264',
       '-pix_fmt', 'yuv420p',
       '-preset', 'ultrafast',
       '-f', 'flv',
       rtmp]
pipe = subprocess.Popen(cmd, shell=False, stdin=subprocess.PIPE)
try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        color_image = np.asanyarray(color_frame.get_data())
        color_colormap_dim = color_image.shape

        # 获取深度信息
        # width = depth_frame.get_width()
        # height = depth_frame.get_height()
        # coordinate = get_coordinate(width / 2, height / 2)
        # print(coordinate)

        # Show images
        # cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        # cv2.imshow('RealSense', color_image)
        # cv2.waitKey(1)
        pipe.stdin.write(color_image.tostring())

finally:

    # Stop streaming
    pipeline.stop()
    pipe.terminate()
