import os
import time
import requests
import mysql.connector
import shutil  # ใช้สำหรับย้ายไฟล์
from datetime import datetime

# ตั้งค่าโฟลเดอร์ที่มีไฟล์รูป
folder_path = "licensePlateFound"
destination_folder = "StudentWithoutHelmet"  # โฟลเดอร์สำหรับย้ายรูปภาพ

# ตรวจสอบว่ามีโฟลเดอร์ปลายทางหรือไม่ ถ้าไม่มีก็สร้างใหม่
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# API URL และ header
url = "https://api.iapp.co.th/license-plate-recognition/file"
headers = {
    'apikey': 'NisHda0fWw0qMtHBicjdIXQa696wn8F9'
}

# เชื่อมต่อกับฐานข้อมูล
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'helmetaidata'
}

# ฟังก์ชันสำหรับดึงข้อมูลจากฐานข้อมูล
def get_license_plates_from_db():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT LicensePlate, StudentID FROM students")
    license_plates = {row[0]: row[1] for row in cursor.fetchall()}  # ใช้ LicensePlate เป็นคีย์และ StudentID เป็นค่า
    cursor.close()
    conn.close()
    return license_plates

# ฟังก์ชันสำหรับตรวจสอบข้อมูล
def check_lp_numbers_against_db(lp_numbers, db_license_plates):
    found_plates = {lp: db_license_plates[lp] for lp in lp_numbers if lp in db_license_plates}
    return found_plates

# ฟังก์ชันสำหรับเพิ่มข้อมูลลงในฐานข้อมูล
def insert_detection_records(detections, found_plates):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # ดึงค่า max_id จากตาราง helmetdetection
    cursor.execute("SELECT MAX(DetectionID) FROM helmetdetection")
    max_id = cursor.fetchone()[0]

    # กำหนด DetectionID ใหม่โดยเพิ่มจาก max_id (เริ่มจาก 1 ถ้าไม่มีข้อมูล)
    new_id = (max_id + 1) if max_id is not None else 1

    now = datetime.now()
    for file_name, lp_number in detections.items():
        # ใช้ found_plates เพื่อดึง student_id ที่ตรงกับ lp_number
        student_id = found_plates.get(lp_number)

        if student_id:  # ตรวจสอบว่ามี student_id หรือไม่
            file_path = os.path.join("http://localhost/thesis_crru_Ai/ai1/StudentWithoutHelmet/", file_name)
            image_url = f"/{file_path}"  # เปลี่ยนให้เป็น URL ของภาพตามต้องการ

            # เพิ่มข้อมูลลงในฐานข้อมูล พร้อมระบุ DetectionID
            cursor.execute("""
                INSERT INTO helmetdetection (DetectionID, StudentID, DetectionTime, ImageURL)
                VALUES (%s, %s, %s, %s)
            """, (new_id, student_id, now, image_url))

            # เพิ่ม new_id สำหรับรายการถัดไป
            new_id += 1

    conn.commit()
    cursor.close()
    conn.close()

# เก็บค่าที่ได้จาก API
lp_numbers = []
file_lp_mapping = {}  # เก็บ mapping ของไฟล์และป้ายทะเบียนที่ตรวจพบ
processed_files = set()  # เก็บไฟล์ที่เคยอ่านแล้ว

# ตัวจับเวลาเริ่มต้น
last_check_time = time.time()

while True:
    # ประมวลผลไฟล์ในโฟลเดอร์
    for file_name in os.listdir(folder_path):
        if file_name.endswith((".jpg", ".png")) and file_name not in processed_files:
            file_path = os.path.join(folder_path, file_name)
            
            # ส่งไฟล์ไปที่ API
            with open(file_path, 'rb') as img_file:
                files = [('file', (file_name, img_file, 'image/jpeg'))]
                response = requests.post(url, headers=headers, files=files)
            
            # ตรวจสอบว่าการส่ง API สำเร็จ
            if response.status_code == 200:
                response_json = response.json()
                lp_number = response_json.get('lp_number', '')

                if lp_number:
                    lp_numbers.append(lp_number)
                    file_lp_mapping[file_name] = lp_number  # เก็บ mapping ของไฟล์และป้ายทะเบียน

                # แสดงค่าที่ได้กลับมา
                print(f"Processed {file_name}: lp_number = {lp_number}")
            else:
                print(f"Error processing {file_name}: {response.status_code} - {response.text}")

            # เพิ่มไฟล์ในรายการที่ประมวลผลแล้ว
            processed_files.add(file_name)

            # หน่วงเวลา 3 วินาที
            time.sleep(3)

    # เช็คข้อมูลกับฐานข้อมูลทุกๆ 1 นาที
    current_time = time.time()
    if current_time - last_check_time >= 60:  # 60 วินาที = 1 นาที
        db_license_plates = get_license_plates_from_db()
        found_plates = check_lp_numbers_against_db(lp_numbers, db_license_plates)
        
        # แสดงค่าใน array ที่ตรงกับฐานข้อมูล
        print("License plates found in database:", found_plates)

        # ย้ายไฟล์ไปยังโฟลเดอร์ปลายทางถ้ามีป้ายทะเบียนในฐานข้อมูล
        detections = {file_name: lp_number for file_name, lp_number in file_lp_mapping.items() if lp_number in found_plates}
        for file_name in detections.keys():
            src_path = os.path.join(folder_path, file_name)
            dst_path = os.path.join(destination_folder, file_name)
            shutil.move(src_path, dst_path)
            print(f"Moved {file_name} to {destination_folder}")

        # เพิ่มข้อมูลลงในตาราง helmetdetection
        insert_detection_records(detections, found_plates)

        # เคลียร์ค่าใน array lp_numbers และ file_lp_mapping
        lp_numbers.clear()
        file_lp_mapping.clear()

        # อัปเดตตัวจับเวลา
        last_check_time = current_time

    # ทำการรอเพื่อวนรอบใหม่
    time.sleep(5)
