import os
from datetime import datetime
from inference_sdk import InferenceHTTPClient
from PIL import Image
import cv2
import numpy as np
import time

# ตั้งค่าเส้นทางของโฟลเดอร์
output_folder = "WithOut Helmet"
temp_folder = "temp_frame"

# ตรวจสอบว่ามีโฟลเดอร์อยู่หรือไม่ ถ้าไม่มีก็สร้างใหม่
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

# เริ่มต้น client สำหรับ inference
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="3Z9EYwLuJCSl5aI6ssqc"
)

# เริ่มต้นการจับภาพจากกล้อง
cap = cv2.VideoCapture(0)  # ใช้หมายเลข 0 เพื่อใช้กล้องหลัก

while True:
    ret, frame = cap.read()
    if not ret:
        print("ไม่สามารถจับภาพจากกล้องได้")
        break

    # แปลงภาพเป็นรูปแบบที่ PIL รองรับ
    pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # แปลงภาพเป็นไฟล์ชั่วคราวเพื่อทำ inference
    temp_image_path = os.path.join(temp_folder, "temp_image.jpg")
    pil_image.save(temp_image_path)

    # ทำ inference กับภาพ
    result = CLIENT.infer(temp_image_path, model_id="helmet-and-non-helmet-abb47/1")
    os.remove(temp_image_path)  # ลบภาพชั่วคราว

    # ตรวจสอบผลลัพธ์
    predictions = result.get('predictions', [])

    # สร้างชื่อไฟล์ที่มีวันที่และเวลาในรูปแบบที่ต้องการ
    timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
    base_filename = f"{timestamp}_WithoutHelmet.jpg"
    output_path = os.path.join(output_folder, base_filename)

    # ตรวจสอบชื่อไฟล์ว่ามีอยู่แล้วหรือไม่ และเพิ่มหมายเลขถ้ามี
    i = 1
    while os.path.exists(output_path):
        new_filename = f"{timestamp}_{i}_WithoutHelmet.jpg"
        output_path = os.path.join(output_folder, new_filename)
        i += 1

    # วนลูปดูผลลัพธ์ของการตรวจจับ
    detected_without_helmet = False
    for prediction in predictions:
        if prediction['class'] == 'Without Helmet':
            detected_without_helmet = True
            print("ไม่สวมหมวก")
            print("ความแม่นยำ:", prediction['confidence'])
            break
        elif prediction['class'] == 'With Helmet':
            print("สวมหมวก")

    # ถ้าพบการตรวจจับว่าไม่สวมหมวกให้บันทึกภาพในช่วงเวลา 0.5 วินาที
    if detected_without_helmet:
        # บันทึกภาพตอนนี้
        pil_image.save(output_path)
        print(f"บันทึกภาพ {output_path}")
        
        # หน่วงเวลา 0.5 วินาทีเพื่อให้แน่ใจว่าภาพที่จับได้เป็นภาพล่าสุด
        time.sleep(0.5)

# ปิดการเชื่อมต่อกล้อง
cap.release()
