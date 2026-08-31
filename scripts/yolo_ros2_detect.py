import cv2
import numpy as np
import onnxruntime as ort
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

# ----------------配置----------------
ONNX_PATH = "./best.onnx"
CLASS_NAMES = ["cup", "mouse", "glasses"]
INPUT_SIZE = 640
CONF_THRESH = 0.4
IOU_THRESH = 0.45

class YoloDetectNode(Node):
    def __init__(self):
        super().__init__("yolo_detect_node")
        self.pub = self.create_publisher(String, "/yolo_detect_result", 10)
        
        self.session = ort.InferenceSession(ONNX_PATH, providers=["CUDAExecutionProvider"])
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

        self.cap = cv2.VideoCapture("/dev/video0")
        # 摄像头硬件参数优化，降低分辨率提帧
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        if not self.cap.isOpened():
            self.get_logger().error("摄像头打开失败")
            raise SystemExit(1)

    def xywh2xyxy(self, x):
        y = np.copy(x)
        y[..., 0] = x[..., 0] - x[..., 2] / 2
        y[..., 1] = x[..., 1] - x[..., 3] / 2
        y[..., 2] = x[..., 0] + x[..., 2] / 2
        y[..., 3] = x[..., 1] + x[..., 3] / 2
        return y

    def nms(self, boxes, scores, iou_thr):
        bboxes_nms = []
        for b in boxes:
            x1, y1, x2, y2 = b
            bboxes_nms.append([int(x1), int(y1), int(x2 - x1), int(y2 - y1)])
        indices = cv2.dnn.NMSBoxes(bboxes_nms, scores.tolist(), 0, iou_thr)
        return indices.flatten() if len(indices) > 0 else []

    def preprocess(self, img):
        h, w = img.shape[:2]
        scale = min(INPUT_SIZE / h, INPUT_SIZE / w)
        nh, nw = int(h * scale), int(w * scale)
        img_res = cv2.resize(img, (nw, nh))
        img_in = np.zeros((INPUT_SIZE, INPUT_SIZE, 3), dtype=np.uint8)
        img_in[:nh, :nw, :] = img_res
        img_in = img_in[..., ::-1].transpose(2, 0, 1).astype(np.float32) / 255.0
        return np.expand_dims(img_in, 0), scale

    def run(self):
        prev_time = time.time()  
        while rclpy.ok():
            ret, frame = self.cap.read()
            if not ret:
                self.get_logger().warn("读帧失败")
                continue

            draw_img = frame.copy()
            blob, scale = self.preprocess(frame)
            out = self.session.run([self.output_name], {self.input_name: blob})[0]
            pred = np.squeeze(out)

            boxes_list = []
            scores_list = []
            clsid_list = []

            for det in pred:
                conf = det[4]
                if conf < CONF_THRESH:
                    continue
                cls_score = det[5:]
                cls_id = int(np.argmax(cls_score))
                boxes_list.append(det[:4])
                scores_list.append(conf)
                clsid_list.append(cls_id)

            pub_str = ""
            if len(boxes_list) > 0:
                boxes_xyxy = self.xywh2xyxy(np.array(boxes_list))
                keep = self.nms(boxes_xyxy, np.array(scores_list), IOU_THRESH)
                pub_str_list = []
                for idx in keep:
                    x1, y1, x2, y2 = boxes_xyxy[idx]
                    x1 = int(x1 / scale)
                    y1 = int(y1 / scale)
                    x2 = int(x2 / scale)
                    y2 = int(y2 / scale)
                    cid = clsid_list[idx]
                    cname = CLASS_NAMES[cid]
                    score = scores_list[idx]
                    pub_str_list.append(f"{cname},{score:.3f},{x1},{y1},{x2},{y2}")
                    cv2.rectangle(draw_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(draw_img, f"{cname} {score:.2f}",
                                (x1, y1 - 6), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 255, 0), 1)
                pub_str = ";".join(pub_str_list)
                msg = String()
                msg.data = ";".join(pub_str_list)
                self.pub.publish(msg)
                # self.get_logger().info(f"发布:{msg.data}") 不要打印提速
            else:
                self.pub.publish(String(data=""))

            # FPS计算
            curr_time = time.time()
            fps = 1.0 / (curr_time - prev_time)
            prev_time = curr_time
            cv2.putText(draw_img, f"FPS:{fps:.1f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # X11弹窗核心
            cv2.imshow("YOLO Detect", draw_img)
            cv2.waitKey(1)

            rclpy.spin_once(self, timeout_sec=0.01)

def main(args=None):
    rclpy.init(args=args)
    node = YoloDetectNode()
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.cap.release()
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
