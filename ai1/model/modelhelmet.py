import cv2
from ultralytics import YOLO
import time
from datetime import datetime
from pathlib import Path

# สร้างโฟลเดอร์สำหรับบันทึกภาพหากยังไม่มี
save_dir = Path('WithOutHelmet')
save_dir.mkdir(parents=True, exist_ok=True)

# รับค่าเลือกว่าจะต้องการแสดงภาพหรือไม่
choice = input("กรุณาเลือก: \n1. แสดงภาพ\n2. ไม่ต้องแสดงภาพ\nเลือก: ")

# โหลดโมเดล YOLOv8 ที่ฝึกฝนไว้
model = YOLO('model/helmet_v2.pt')  # เปลี่ยน path ให้ตรงกับที่เก็บโมเดลของคุณ

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
        detections = result.boxes.xyxy  # ตำแหน่งกรอบ
        confidences = result.boxes.conf  # ความเชื่อมั่น
        classes = result.boxes.cls  # คลาส

        for i in range(len(detections)):
            class_id = int(classes[i].item())  # ID ของคลาส
            confidence = confidences[i].item()  # ความเชื่อมั่น
            label = model.names[class_id] if class_id < len(model.names) else 'Unknown'  # ชื่อของคลาส (label)

            # พิมพ์ผลลัพธ์
            print(f"Class ID: {class_id}, Confidence: {confidence:.2f}, Label: {label}")

            # ตรวจสอบว่าไม่สวมหมวกกันน็อค
            if label != 'With Helmet':  # เปลี่ยน 'With Helmet' ให้ตรงกับคลาสของหมวกกันน็อคที่ต้องการ
                # สร้างชื่อไฟล์ที่มีวันที่และเวลา
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                image_filename = save_dir / f'{timestamp}_WithoutHelmet.jpg'

                # ดึงพิกัดของกรอบ
                x1, y1, x2, y2 = map(int, detections[i])

                # วาดกรอบและข้อความลงบนภาพ
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # วาดกรอบสีเขียว
                cv2.putText(frame, f'{label} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  # วาดข้อความ

                # บันทึกภาพไปยังโฟลเดอร์ WithOutHelmet
                cv2.imwrite(str(image_filename), frame)
                print(f"Saved image: {image_filename}")

    # หากเลือก 1 ให้แสดงภาพที่มีการวาดกรอบและข้อความ
    if choice == '1':
        cv2.imshow('Helmet Detection', frame)

    # เพิ่มดีเลย์ 0.5 วินาที
    time.sleep(0.5)

    # ตรวจสอบการกดปุ่ม 'q' เพื่อออกจากลูป
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ปิดกล้องและหน้าต่างที่แสดงหากมีการแสดงภาพ
cap.release()
if choice == '1':
    cv2.destroyAllWindows()
