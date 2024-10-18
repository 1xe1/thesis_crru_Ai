import cv2
from ultralytics import YOLO
from datetime import datetime
from pathlib import Path
import os
import time
import tkinter as tk
from tkinter import ttk
from tkinter import Scale
from PIL import Image, ImageTk

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

# ฟังก์ชันตรวจจับหมวกกันน็อค
def detect_helmet(frame, confidence_threshold):
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

            # ตรวจสอบความแม่นยำตามค่าที่ตั้งไว้
            if confidence >= confidence_threshold and label != 'With Helmet':  # สมมติว่าคลาส 'With Helmet' หมายถึงใส่หมวกกันน็อค
                no_helmet = True
                # วาดกรอบบนภาพ
                x1, y1, x2, y2 = map(int, detections[i])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # สีแดงสำหรับไม่ใส่หมวกกันน็อค
                cv2.putText(frame, f'{"Helmet"} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

    return no_helmet, frame

def detect_license_plate(image_path):
    """ตรวจจับป้ายทะเบียน"""
    frame = cv2.imread(str(image_path))  # อ่านภาพจากไฟล์
    results = plate_model(frame)  # ตรวจจับป้ายทะเบียน
    found_plate = False  # ตัวแปรสำหรับตรวจสอบว่าพบหรือไม่
    confidence_threshold = 0.45  # กำหนดค่าความแม่นยำ 45%

    for result in results:
        detections = result.boxes.xyxy  # ตำแหน่งกรอบ
        confidences = result.boxes.conf  # ความเชื่อมั่น
        classes = result.boxes.cls  # คลาส

        for i in range(len(detections)):
            class_id = int(classes[i].item())
            confidence = confidences[i].item()
            label = plate_model.names[class_id] if class_id < len(plate_model.names) else 'Unknown'

            # ตรวจสอบค่าความแม่นยำต้องมากกว่า 45% และคลาสเป็นป้ายทะเบียน
            if confidence >= confidence_threshold and label == 'License_Plate':  # ตรวจสอบว่าพบป้ายทะเบียน
                found_plate = True
                # วาดกรอบและข้อความลงบนภาพ
                x1, y1, x2, y2 = map(int, detections[i])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{"License Plate"} {confidence:.2f}', (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

    return found_plate, frame


# ฟังก์ชันสำหรับอัพเดตภาพจากกล้อง
def update_frame():
    ret, frame = cap.read()  # อ่านภาพจากกล้อง
    if not ret:
        print("ไม่สามารถอ่านภาพจากกล้องได้")
        return

    # ปรับค่าความแม่นยำที่ผู้ใช้เลือก
    confidence_threshold = confidence_scale.get() / 100

    # ตรวจจับหมวกกันน็อค
    no_helmet, processed_frame = detect_helmet(frame, confidence_threshold)

    # บันทึกภาพถ้าพบผู้ไม่ใส่หมวกกันน็อค
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

    # แสดงภาพใน GUI
    img = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)
    video_panel.imgtk = imgtk
    video_panel.config(image=imgtk)

    root.after(300, update_frame)

# สร้างหน้าต่าง GUI
root = tk.Tk()
root.title("Helmet and License Plate Detection")

# สไตล์ทั่วไป
root.configure(bg="#2C3E50")

# สร้างเลย์เอาต์หลัก: ซ้ายสำหรับการปรับค่าความแม่นยำ, ขวาสำหรับแสดงภาพ
main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill="both", expand=True)

# กำหนดสไตล์ ttk
style = ttk.Style()
style.configure("TFrame", background="#2C3E50")
style.configure("TLabel", background="#2C3E50", foreground="white", font=("Arial", 12))
style.configure("TScale", background="#2C3E50")

# แถบเลื่อนปรับความแม่นยำ
control_frame = ttk.Frame(main_frame, style="TFrame")
control_frame.pack(side="left", fill="y", padx=10)

ttk.Label(control_frame, text="ค่าความแม่นยำของการตรวจจับหมวกกันน็อค", style="TLabel").pack(pady=10)
confidence_scale = Scale(control_frame, from_=0, to=100, orient="horizontal", length=200, bg="#34495E", fg="white", highlightbackground="#34495E")
confidence_scale.set(50)  # ตั้งค่าเริ่มต้นที่ 50%
confidence_scale.pack(pady=20)

# พื้นที่แสดงภาพ
video_panel = ttk.Label(main_frame, style="TLabel")
video_panel.pack(side="right", fill="both", expand=True)

# เริ่มการอัพเดตภาพ
update_frame()

# เริ่มต้น GUI
root.mainloop()

# ปิดการใช้งานกล้องเมื่อปิด GUI
cap.release()
cv2.destroyAllWindows()