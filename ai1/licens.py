import cv2
import os
import time
from ultralytics import YOLO

# โหลดโมเดล YOLOv8 ที่ฝึกฝนไว้
model = YOLO('model/licens_v2.pt')  # เปลี่ยน path ให้ตรงกับที่เก็บโมเดลของคุณ

# โฟลเดอร์ที่เก็บรูปภาพ
image_folder = 'WithOutHelmet'

# เก็บรายการไฟล์ที่ประมวลผลไปแล้ว
processed_files = set()

# ฟังก์ชันตรวจจับจากภาพในโฟลเดอร์
def detect_from_folder():
    while True:
        # ดึงรายชื่อไฟล์ทั้งหมดในโฟลเดอร์ที่เป็นไฟล์รูปภาพ
        image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

        # ตรวจสอบว่าไฟล์รูปภาพมีไฟล์ใหม่ที่ยังไม่ประมวลผลหรือไม่
        new_files = [f for f in image_files if f not in processed_files]

        if new_files:
            for image_file in new_files:
                image_path = os.path.join(image_folder, image_file)

                # อ่านรูปภาพจากไฟล์
                frame = cv2.imread(image_path)
                if frame is None:
                    print(f"ไม่สามารถเปิดรูปภาพ {image_file} ได้")
                    continue

                # ทำการตรวจจับ
                detect(frame)

                # เพิ่มไฟล์ที่ประมวลผลไปแล้วลงใน processed_files
                processed_files.add(image_file)
        else:
            print("ไม่มีไฟล์ใหม่ในโฟลเดอร์ รอการเพิ่มรูปภาพ...")

        # เพิ่มดีเลย์ 0.5 วินาที
        time.sleep(0.5)

# ฟังก์ชันตรวจจับจากกล้อง
def detect_from_camera():
    cap = cv2.VideoCapture(0)  # เปิดกล้อง
    if not cap.isOpened():
        print("ไม่สามารถเปิดกล้องได้")
        return
    
    while True:
        ret, frame = cap.read()  # อ่านภาพจากกล้อง
        if not ret:
            print("ไม่สามารถอ่านภาพจากกล้องได้")
            break

        # ทำการตรวจจับ
        detect(frame)

        # แสดงภาพผลลัพธ์
        cv2.imshow('Frame', frame)

        # กด 'q' เพื่อออกจากการแสดงผล
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # เพิ่มดีเลย์ 0.5 วินาที
        time.sleep(0.5)

    cap.release()
    cv2.destroyAllWindows()

# ฟังก์ชันทำการตรวจจับและแสดงผลลัพธ์
def detect(frame):
    # ทำการตรวจจับ
    results = model(frame)

    # ตรวจสอบว่ามีผลลัพธ์หรือไม่
    license_plate_found = False
    if results:
        result = results[0]  # ใช้ผลลัพธ์แรกจากการตรวจจับ (YOLOv8)
        
        if result.boxes:  # ตรวจสอบว่ามีการตรวจจับกรอบหรือไม่
            detections = result.boxes.xyxy  # ตำแหน่งของกรอบ
            confidences = result.boxes.conf  # ความเชื่อมั่นของแต่ละกรอบ
            classes = result.boxes.cls  # คลาสที่ตรวจจับได้

            for i in range(len(detections)):
                class_id = int(classes[i].item())  # ID ของคลาส
                confidence = confidences[i].item()  # ความเชื่อมั่น
                label = model.names[class_id] if class_id < len(model.names) else 'Unknown'  # ชื่อของคลาส (label)

                # ดึงพิกัดของกรอบ
                x1, y1, x2, y2 = map(int, detections[i])  # แปลงตำแหน่งให้เป็น int

                # วาดกรอบบนภาพ (สีเขียว)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # วาดข้อความ (ชื่อคลาสและความเชื่อมั่น) บนภาพ
                cv2.putText(frame, f'{label} {confidence:.2f}', (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # ถ้าตรวจจับว่าเป็น License Plate
                if label == 'License_Plate':
                    license_plate_found = True

                # พิมพ์ผลลัพธ์ลงใน console
                print(f"Class ID: {class_id}, Confidence: {confidence:.2f}, Label: {label}")

    if license_plate_found:
        print("ป้ายทะเบียนพบในภาพ")

# ส่วนหลักของโปรแกรม
print("เลือกโหมดการทำงาน:")
print("1. ตรวจจับจากกล้อง")
print("2. ตรวจจับจากโฟลเดอร์")

mode = input("กรุณากดหมายเลขโหมดการทำงาน (1 หรือ 2): ")

if mode == '1':
    detect_from_camera()
elif mode == '2':
    detect_from_folder()
else:
    print("เลือกโหมดไม่ถูกต้อง")
