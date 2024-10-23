import cv2
import numpy as np
import os

#=============== ตัวแปรสำหรับเมาส์ ==================#
drawing = False           # ตัวแปรเพื่อเก็บสถานะการวาด (False = ยังไม่วาด)
moving_corner = False     # ตัวแปรเพื่อเก็บสถานะการขยับมุม
selected_corner = None    # มุมที่ถูกเลือกเพื่อขยับ
point1 = ()               # เก็บจุดเริ่มต้นของการวาดเส้น
point2 = ()               # เก็บจุดสิ้นสุดของการวาดเส้น
roi_defined = False       # เช็คว่า ROI ถูกวาดแล้วหรือยัง
#================================================#

# ฟังก์ชันสำหรับจับการเคลื่อนไหวของเมาส์
def mouse_drawing(event, x, y, flags, params):
    global point1, point2, drawing, moving_corner, selected_corner, roi_defined

    def is_near(a, b, threshold=5):
        return abs(a - b) < threshold

    def get_corner(point1, point2, x, y):
        if is_near(point1[0], x) and is_near(point1[1], y):
            return "point1"
        elif is_near(point2[0], x) and is_near(point2[1], y):
            return "point2"
        elif is_near(point1[0], x) and is_near(point2[1], y):
            return "point1_bottom"
        elif is_near(point2[0], x) and is_near(point1[1], y):
            return "point2_top"
        return None

    if event == cv2.EVENT_LBUTTONDOWN:
        if roi_defined:
            selected_corner = get_corner(point1, point2, x, y)
            if selected_corner:
                moving_corner = True
        else:
            drawing = True
            point1 = (x, y)
            point2 = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            point2 = (x, y)
        elif moving_corner:
            if selected_corner == "point1":
                point1 = (x, y)
            elif selected_corner == "point2":
                point2 = (x, y)
            elif selected_corner == "point1_bottom":
                point1 = (x, point1[1])
                point2 = (point2[0], y)
            elif selected_corner == "point2_top":
                point1 = (point1[0], y)
                point2 = (x, point2[1])

    elif event == cv2.EVENT_LBUTTONUP:
        if drawing:
            drawing = False
            roi_defined = True
        elif moving_corner:
            moving_corner = False

def is_box_in_roi(box, roi):
    x, y, w, h = box
    roi_x1, roi_y1, roi_x2, roi_y2 = roi
    box_x2 = x + w
    box_y2 = y + h

    # ตรวจสอบการซ้อนทับระหว่างกล่องกับ ROI
    return not (box_x2 < roi_x1 or x > roi_x2 or box_y2 < roi_y1 or y > roi_y2)

def detect_cars_in_camera(camera_index=0):
    global roi_defined, point1, point2
    # กำหนดพาธของไฟล์ที่จำเป็น
    current_dir = os.path.dirname(os.path.abspath(__file__))
    weights_path = os.path.join(current_dir, "yolov3.weights")
    config_path = os.path.join(current_dir, "yolov3.cfg")
    classes_path = os.path.join(current_dir, "coco.names")

    # โหลดโมเดล YOLOv3 ที่ผ่านการเทรนมาแล้ว
    net = cv2.dnn.readNet(weights_path, config_path)
    
    # โหลดชื่อคลาสจากไฟล์ coco.names
    with open(classes_path, "r") as f:
        classes = [line.strip() for line in f.readlines()]
    
    # เปิดการเชื่อมต่อกับกล้องตาม camera_index ที่ผู้ใช้เลือก
    cap = cv2.VideoCapture(camera_index)

    # สร้างหน้าต่างสำหรับแสดงผล และเชื่อมต่อฟังก์ชันจับเมาส์
    cv2.namedWindow("Car Detection")
    cv2.setMouseCallback("Car Detection", mouse_drawing)

    def process_frame(frame):
        height, width, _ = frame.shape

        # สร้าง blob จากภาพ
        blob = cv2.dnn.blobFromImage(frame, 1/255, (320, 320), (0, 0, 0), True, crop=False)
        
        # ส่ง blob เข้าสู่โมเดล
        net.setInput(blob)
        outs = net.forward(net.getUnconnectedOutLayersNames())
        
        # ประมวลผลการตรวจจับ
        class_ids = []
        confidences = []
        boxes = []
        
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5 and classes[class_id] == "car":
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    
                    # ตรวจสอบว่ากล่องตรวจจับรถมีส่วนหนึ่งส่วนใดอยู่ใน ROI หรือไม่
                    roi = (point1[0], point1[1], point2[0], point2[1])
                    if is_box_in_roi((x, y, w, h), roi):
                        class_ids.append(class_id)
                        confidences.append(float(confidence))
                        boxes.append([x, y, w, h])
        
        # ใช้ Non-Maximum Suppression เพื่อลดการตรวจจับซ้ำซ้อน
        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        
        # นับจำนวนรถที่ตรวจพบใน ROI
        car_count = len(indices)
        
        # วาดกรอบรอบรถที่ตรวจพบใน ROI
        for i in indices:
            box = boxes[i]
            x, y, w, h = box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"Car {confidences[i]:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # วาดกรอบสี่เหลี่ยม ROI บนภาพ
        cv2.rectangle(frame, point1, point2, (100, 50, 200), 2)
        # แสดงจำนวนรถที่มุมล่างของ ROI
        cv2.putText(frame, f"Number of cars: {car_count}", (point1[0], point2[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 50, 200), 2)
        
        return frame

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # ปรับขนาดเฟรมเป็น 320x240
        frame = cv2.resize(frame, (320, 240))

        temp_frame = frame.copy()
        if point1 and point2:
            cv2.rectangle(temp_frame, point1, point2, (100, 50, 200), 2)

        cv2.imshow("Car Detection", temp_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q') or roi_defined:
            break
    
    if not roi_defined:
        cap.release()
        cv2.destroyAllWindows()
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # ปรับขนาดเฟรมเป็น 320x240
        frame = cv2.resize(frame, (320, 240))

        # ประมวลผลเฟรม
        frame = process_frame(frame)

        # แสดงผลลัพธ์
        cv2.imshow("Car Detection", frame)
        
        # เพิ่มดีเลย์ให้การแสดงผลเฟรมแต่ละเฟรมเพื่อให้วิดีโอเล่นที่ความเร็วปกติ
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # ใส่หมายเลขกล้องที่ต้องการ เช่น 0, 1, 2, ...
    camera_index = 0
    detect_cars_in_camera(camera_index)
