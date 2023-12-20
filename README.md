# cv-camera

#### 介绍

    基于yolov5的训练模型，使用tensorrt在边缘设备上对多路摄像头进行帧流数据分析的一套集成系统。仅需替换模型和修改参数，即可对多路摄像头设备进行帧流数据分析，并可将捕捉到的报警图片上传至指定服务器设备进行。

#### 软件架构

    基于ARM架构，在 Jetson Nano 已做充分测试。

#### 部署说明

    使用的是`jp46` 版本Jetson Nano镜像，为避免官网下载过慢以及镜像更新过快，这里给出百度云镜像下载链接：

`链接: https://pan.baidu.com/s/1Sg5Srh6xJAG880_i_7ePqg 提取码: g1g9 `

##### 直接部署

1. 安装相关依赖包 pycuda, torch, torchvision, flask, flask_sqlalchemy, tensorrt
2. 转换模型，需要先将模型转为`wts` 模型，具体转换方法可参考[tensorrtx/yolov5 at master · wang-xinyu/tensorrtx · GitHub](https://github.com/wang-xinyu/tensorrtx/tree/master/yolov5)，在Jetson Nano上`engine` 模型具体转换如下：
   
   ```
   # 克隆代码
   git clone https://gitee.com/zbx996/cv-camera.git
   
   
   # 修改类数目
   # 修改 yololayer.h 文件中 CLASS_NUM 值为模型类目数
   # 编译
   cd lib
   mkdir build
   cd build
   cmake ..
   make
   
   # 模型转换
   sudo ./yolov5 -s 'wts模型路径' yolov5s.engine s
   ```

##### docker部署（推荐）

```
# 下载打包好的 docker 镜像
wget http://cv-file.test.upcdn.net/cv-camera.tar


# 加载镜像
sudo docker load -i cv-camera.tar


# 创建容器
sudo docker run --gpus all -it --name cv -p '需要映射的端口号':5000 '镜像id'


# 克隆代码
git clone https://gitee.com/zbx996/cv-camera.git


# 模型转换等同上操作
```

        成功运行后可在局域网中以`ip:端口` 方式访问，以进行相关设置。

<img title="" src="https://gitee.com/zbx996/drawing-bed/raw/master/examp.png" alt="" width="647" data-align="center">

#### 使用说明

1. 摄像头编号：唯一id
2. 摄像头地址：RTSP视频流地址
3. 摄像头位置：摄像头布置位置
4. 图片上传地址：检测到的报警图片上传地址
5. 检测等级：同配置`config.py` 文件中`categories` 值的索引对应，`1` 即代表只检`categories`值中的第一个类别，其余类别不检测、不标记、不报警上传
6. 时间间隔：每路摄像头检测时间间隔
