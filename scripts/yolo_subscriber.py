import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class YoloResultSub(Node):
    def __init__(self):
        super().__init__("yolo_result_sub")
        self.sub = self.create_subscription(
            String,
            "/yolo_detect_result",
            self.callback,
            10
        )
        self.get_logger().info("订阅节点已启动，等待检测结果...")

    def callback(self, msg):
        data = msg.data
        if not data:
            # 空字符串，没有检测到物体
            return
        # 分号分割多个目标
        obj_list = data.split(";")
        for obj_str in obj_list:
            parts = obj_str.split(",")
            cname = parts[0]          # 类别名 cup/mouse/glasses
            score = float(parts[1])   # 置信度
            x1 = int(parts[2])
            y1 = int(parts[3])
            x2 = int(parts[4])
            y2 = int(parts[5])
            # 计算物体像素中心点
            cx = (x1 + x2) / 2.0
            cy = (y1 + y2) / 2.0
            w = x2 - x1
            h = y2 - y1
            self.get_logger().info(
                f"物体:{cname} | 置信:{score:.2f} | 框[{x1},{y1},{x2},{y2}] | 中心({cx:.1f},{cy:.1f}) | 宽高({w},{h})"
            )

def main(args=None):
    rclpy.init(args=args)
    node = YoloResultSub()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
