import cv2
from ultralytics import YOLO
from datetime import datetime
from pathlib import Path
import os
import time

# สร้างโฟลเดอร์ต่างๆ หากยังไม่มี
helmet_dir = Path('WithOutHelmet')
plate_found_dir = Path('licensePlateFound')
warning_dir = Path('warning')

helmet_dir.mkdir(parents=True, exist_ok=True)
plate_found_dir.mkdir(parents=True, exist_ok=True)
warning_dir.mkdir(parents=True, exist_ok=True)

# โหลดโมเดล YOLOv8 สำหรับตรวจจับหมวกกันน็อคและป้ายทะเบียน
helmet_model = YOLO('model/helmet_v2.pt')  # โมเดลตรวจจับหมวกกันน็อค
plate_model = YOLO('model/licens_v2.pt')  # โมเดลตรวจจับป้ายทะเบียน

# เปิดกล้อง
cap = cv2.VideoCapture(0)  # เปิดกล้อง (0 สำหรับกล้องหลัก)

# ถามผู้ใช้ว่าอยากแสดงภาพหรือไม่
user_input = input("กรุณาเลือก: (1) ไม่แสดงภาพ (2) แสดงภาพ: ")

# ตรวจสอบการเลือกของผู้ใช้
if user_input == '1':
    show_image = False
    print("ตั้งค่า: ไม่แสดงภาพ")
elif user_input == '2':
    show_image = True
    print("ตั้งค่า: แสดงภาพ")
else:
    print("เลือกไม่ถูกต้อง ระบบจะตั้งค่าเป็นไม่แสดงภาพโดยอัตโนมัติ")
    show_image = False

def detect_helmet(frame):
    """ตรวจจับหมวกกันน็อค"""
    results = helmet_model(frame)  # ตรวจจับหมวกกันน็อค
    no_helmet = False  # ตัวแปรสำหรับตรวจสอบว่าพบหรือไม่
    for result in results:
        detections = result.boxes.xyxy  # ตำแหน่งกรอบ
        confidences = result.boxes.conf  # ความเชื่อมั่น
        classes = result.boxes.cls  # คลาส
        for i in range(len(detections)):
            class_id = int(classes[i].item())
            confidence = confidences[i].item()
            label = helmet_model.names[class_id] if class_id < len(helmet_model.names) else 'Unknown'

            # ตรวจสอบว่าคนไม่ใส่หมวกกันน็อค
            if label != 'With Helmet':  # สมมติว่าคลาส 'With Helmet' หมายถึงใส่หมวกกันน็อค
                no_helmet = True
                # วาดกรอบบนภาพ
                x1, y1, x2, y2 = map(int, detections[i])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # สีแดงสำหรับไม่ใส่หมวกกันน็อค
                cv2.putText(frame, f'{label} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    return no_helmet, frame

def detect_license_plate(image_path):
    """ตรวจจับป้ายทะเบียน"""
    frame = cv2.imread(str(image_path))  # อ่านภาพจากไฟล์
    results = plate_model(frame)  # ตรวจจับป้ายทะเบียน
    found_plate = False  # ตัวแปรสำหรับตรวจสอบว่าพบหรือไม่

    for result in results:
        detections = result.boxes.xyxy  # ตำแหน่งกรอบ
        confidences = result.boxes.conf  # ความเชื่อมั่น
        classes = result.boxes.cls  # คลาส

        for i in range(len(detections)):
            class_id = int(classes[i].item())
            confidence = confidences[i].item()
            label = plate_model.names[class_id] if class_id < len(plate_model.names) else 'Unknown'

            if label == 'License_Plate':  # ตรวจสอบว่าพบป้ายทะเบียน
                found_plate = True
                # วาดกรอบและข้อความลงบนภาพ
                x1, y1, x2, y2 = map(int, detections[i])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{label} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return found_plate, frame

while True:
    ret, frame = cap.read()  # อ่านภาพจากกล้อง
    if not ret:
        print("ไม่สามารถอ่านภาพจากกล้องได้")
        break

    # ตรวจจับหมวกกันน็อค
    no_helmet, processed_frame = detect_helmet(frame)

    if no_helmet:
        # สร้างชื่อไฟล์และบันทึกภาพในโฟลเดอร์ WithOutHelmet
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        image_filename = helmet_dir / f'{timestamp}_WithoutHelmet.jpg'
        cv2.imwrite(str(image_filename), processed_frame)
        print(f"บันทึกภาพที่ {image_filename}")

        # ตรวจจับป้ายทะเบียนจากภาพที่บันทึกไว้
        found, license_frame = detect_license_plate(image_filename)

        if found:
            # บันทึกภาพที่ตรวจจับป้ายทะเบียนได้ในโฟลเดอร์ licensePlateFound
            new_filename = plate_found_dir / f'{timestamp}_WithoutHelmet_licensePlate.jpg'
            cv2.imwrite(str(new_filename), license_frame)
            print(f"ป้ายทะเบียนพบ: บันทึกภาพที่ {new_filename}")
        else:
            # บันทึกภาพในโฟลเดอร์ warning หากไม่พบป้ายทะเบียน
            new_filename = warning_dir / f'{timestamp}_warning.jpg'
            cv2.imwrite(str(new_filename), license_frame)
            print(f"ไม่พบป้ายทะเบียน: บันทึกภาพที่ {new_filename}")

        # ลบภาพเดิมในโฟลเดอร์ WithOutHelmet หลังจากบันทึกแล้ว
        try:
            os.remove(image_filename)  # ลบไฟล์
            print(f"ลบไฟล์เดิม: {image_filename}")
        except Exception as e:
            print(f"ข้อผิดพลาดในการลบไฟล์: {e}")

    # แสดงผลลัพธ์แบบเรียลไทม์ถ้าการตั้งค่าเปิดการแสดงภาพอยู่
    if show_image:
        cv2.imshow('Helmet Detection', processed_frame)
        
    # ดีเลย์ 1 วินาทีต่อการตรวจจับ
    time.sleep(1)

# ปิดการใช้งานกล้อง
cap.release()
cv2.destroyAllWindows()
