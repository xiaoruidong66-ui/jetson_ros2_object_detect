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

训练权重 best.pt



\## JETSON部署

1\. 将best.pt转为TensorRT engine模型

2\. 运行ROS2节点完成目标检测推理

