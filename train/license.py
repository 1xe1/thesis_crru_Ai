import cv2
from ultralytics import YOLO
import time

# โหลดโมเดล YOLOv8 ที่ฝึกฝนไว้
model = YOLO('model/helmet.pt')  # เปลี่ยน path ให้ตรงกับที่เก็บโมเดลของคุณ

# เปิดกล้อง
cap = cv2.VideoCapture(0)  # 0 สำหรับกล้องหลัก

while True:
    # อ่านภาพจากกล้อง
    ret, frame = cap.read()
    if not ret:
        print("ไม่สามารถอ่านภาพจากกล้องได้")
        break

    # ทำการตรวจจับ
    results = model(frame)

    # ดึงข้อมูลการตรวจจับ
    for result in results:
        detections = result.boxes.xyxy
        confidences = result.boxes.conf
        classes = result.boxes.cls

        for i in range(len(detections)):
            class_id = int(classes[i].item())  # ID ของคลาส
            confidence = confidences[i].item()  # ความเชื่อมั่น
            label = model.names[class_id] if class_id < len(model.names) else 'Unknown'  # ชื่อของคลาส (label)

            # พิมพ์ผลลัพธ์
            print(f"Class ID: {class_id}, Confidence: {confidence:.2f}, Label: {label}")

    # เพิ่มดีเลย์ 0.5 วินาที
    time.sleep(0.5)

    # ตรวจสอบการกดปุ่ม 'q' เพื่อออกจากลูป
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ปิดกล้องและหน้าต่างที่แสดง
cap.release()
cv2.destroyAllWindows()
