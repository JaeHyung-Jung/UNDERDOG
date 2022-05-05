- 카메라 확인

```
  gst-launch-1.0 nvarguscamerasrc sensor_mode=0 ! 'video/x-raw(memory:NVMM),width=3820, height=2464, framerate=21/1, format=NV12' ! nvvidconv flip-method=0 ! 'video/x-raw,width=960, height=616' ! nvvidconv ! nvegltransform ! nveglglessink -e
```

```
    DISPLAY=:0.0 gst-launch-1.0 nvarguscamerasrc ! 'video/x-raw(memory:NVMM), width=3280, height=2464, format=(string)NV12, framerate=(fraction)20/1' ! nvoverlaysink -e
```

```
    // 자주색 화면 일때
    wget https://www.waveshare.com/w/upload/e/eb/Camera_overrides.tar.gz
    tar zxvf Camera_overrides.tar.gz
    sudo cp camera_overrides.isp /var/nvidia/nvcam/settings/
    sudo chmod 664 /var/nvidia/nvcam/settings/camera_overrides.isp
    sudo chown root:root /var/nvidia/nvcam/settings/camera_overrides.isp
```
