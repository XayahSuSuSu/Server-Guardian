# 瞩暮行者 - 服务器端
> 环境：Docker

## 一、搭建RTMP服务器
### 拉取`nginx-rtmp`镜像
```
docker pull alfg/nginx-rtmp
```

### 创建并运行`nginx-rtmp`容器
```
docker run -itd --name nginx-rtmp -p 3308:1935 alfg/nginx-rtmp
```

### 推流（OBS Studio）
以`rtmp://127.0.0.1:3308/stream/record`为例

服务器：
```
rtmp://127.0.0.1:3308/stream
```

串流密钥：
```
record
```

![推流设置](images/推流设置.png "推流设置")

### 测试（PotPlayer）
打开链接

![测试0](images/测试0.png "测试0")

查看RTMP流

![测试1](images/测试1.png "测试1")

### 推流（OpenCV）
以`rtmp://127.0.0.1:3308/stream/car`为例

修改`PushRTMP.py`中的`rtmp`变量为推流地址
```
rtmp = r'rtmp://127.0.0.1:33308/stream/car'
```

运行`PushRTMP.py`
```
python PushRTMP.py
```

### RTSP流转RTMP流（FFmpeg）
以`rtsp://admin:123456@192.168.1.56:554/ch01.264` → `rtmp://127.0.0.1:33308/stream/court`为例
安装**FFmpeg**并再用其转流

```
ffmpeg -i "rtsp://admin:123456@192.168.1.56:554/ch01.264" -vcodec copy -acodec copy -f flv "rtmp://127.0.0.1:33308/stream/court"
```
