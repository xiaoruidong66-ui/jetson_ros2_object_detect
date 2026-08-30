\# jetson\_ros2\_object\_detect

YOLOv5目标检测实验项目



\## 项目说明

本仓库存放自制数据集、实验截图、ROS2业务代码。

本模型实现三类目标检测：杯子、鼠标、眼镜。

YOLOv5原始源码不在本仓库，请自行下载官方YOLOv5。



\## 环境准备

1\. 下载YOLOv5源码：https://github.com/ultralytics/yolov5

2\. Python依赖按照YOLOv5官方requirements.txt安装

3\. 训练权重best.pt



\## 目录结构

jetson\_ros2\_object\_detect

├── README.md           # 项目说明

├── dataset             # 自制数据集 (images + labels)

├── src                 # ROS2 节点代码

└── test\_case           # 实验截图、测试结果

&#x20;

\## 训练步骤

1\. 将dataset里的数据集复制到YOLOv5工程目录下

2\. 修改yaml数据集配置文件

3\. 运行train.py开始模型训练



\## 训练结果

检测类别：杯子、鼠标、眼镜

训练曲线图、PR曲线、验证集检测效果图存放于 test\_case 文件夹。

训练权重 best.pt：本仓库不存放模型权重文件。权重生成路径为 yolov5‑master/runs/train/exp5/weights/best.pt，部署时使用MobaXterm传输至Jetson Nano开发板使用。



\## 数据集制作

\- 使用LabelImg工具对图片进行标注，生成xml标签，转换为yolo格式txt标签。

\- 使用本仓库scripts目录下的划分脚本，自动将数据集切分为训练集、验证集。



\## 运行环境与依赖

训练平台：PC端，YOLOv5‑v7.0

依赖：PyTorch, torchvision, opencv‑python, numpy

开发板部署平台：Jetson Nano

部署依赖：JetPack, TensorRT, ROS2, pycuda



复现步骤：

1\. clone YOLOv5官方代码仓库

2\. 使用LabelImg进行标注，或者直接使用本仓库dataset数据集；可运行scripts下的划分脚本拆分训练/验证集

3\. 使用config中的yaml配置文件

4\. 执行训练得到best.pt权重

5\. 通过MobaXterm将权重传输至Jetson Nano，导出TensorRT engine模型进行推理



\## ROS2推理节点

ROS2推理代码待开发，部署于Jetson Nano开发板，实现摄像头读取、目标检测、检测框话题发布。



\## JETSON部署

1\. 将best.pt转为TensorRT engine模型

2\. 运行ROS2节点完成目标检测推理

