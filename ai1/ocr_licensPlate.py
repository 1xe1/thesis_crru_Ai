import os
import time
import requests
import mysql.connector
from mysql.connector import pooling
import shutil
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
    # 'apikey': 'Q4B0VZLUQJt9ecrg3YoOoD8SadfZKZqr'
    'apikey': 'ZFZP6321GHimv6S9W499ceslrFO9vtgB'
    # 'apikey': 'yZH8V3McJdEX5PN560yxZeOhiCCVFzLm'
    # 'apikey': 'GyTS2CyNM9qR3MG9yXXmL5SgRfmXsofE'
    # 'apikey': 'AxKdELhF6t2gST2Hy1BhAfEFejrL8hzD'
    # 'apikey': 'CV13kBFVxmkdzRMGQBaN0tl3NjGmhxGD'
    # 'apikey': 'p516kGj8PdOtO1EnlSp27FCJfk8CtaaE'
}

# ตั้งค่า database connection pool
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'helmetaidata',
    'pool_name': 'mypool',
    'pool_size': 5
}

db_pool = pooling.MySQLConnectionPool(**db_config)

# ฟังก์ชันสำหรับดึงข้อมูลจากฐานข้อมูล
def get_license_plates_from_db():
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT LicensePlate, StudentID FROM students")
        license_plates = {row[0]: row[1] for row in cursor.fetchall()}
        cursor.close()
        conn.close()
        return license_plates
    except mysql.connector.Error as err:
        print(f"Error fetching license plates from DB: {err}")
        return {}

# ฟังก์ชันสำหรับตรวจสอบข้อมูล
def check_lp_numbers_against_db(lp_numbers, db_license_plates):
    found_plates = {lp: db_license_plates[lp] for lp in lp_numbers if lp in db_license_plates}
    return found_plates

# ฟังก์ชันสำหรับเพิ่มข้อมูลลงในฐานข้อมูล
def insert_detection_records(detections, found_plates):
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT MAX(DetectionID) FROM helmetdetection")
        max_id = cursor.fetchone()[0]
        new_id = (max_id + 1) if max_id is not None else 1

        now = datetime.now()
        for file_name, lp_number in detections.items():
            student_id = found_plates.get(lp_number)
            if student_id:
                file_path = os.path.join("http://localhost/thesis_crru_Ai/ai1/StudentWithoutHelmet/", file_name)
                image_url = f"{file_path}"

                cursor.execute("""
                    INSERT INTO helmetdetection (DetectionID, StudentID, DetectionTime, ImageURL)
                    VALUES (%s, %s, %s, %s)
                """, (new_id, student_id, now, image_url))

                new_id += 1

        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error inserting detection records: {err}")

# ฟังก์ชันสำหรับส่งไฟล์ไปที่ API และ retry กรณีล้มเหลว
def send_image_to_api(file_path, file_name):
    max_retries = 3
    retry_delay = 2  # seconds
    for attempt in range(max_retries):
        try:
            with open(file_path, 'rb') as img_file:
                files = [('file', (file_name, img_file, 'image/jpeg'))]
                response = requests.post(url, headers=headers, files=files)

            if response.status_code == 200:
                response_json = response.json()
                return response_json.get('lp_number', '')
            else:
                print(f"Error processing {file_name}: {response.status_code} - {response.text}")
                return None
        except requests.RequestException as e:
            print(f"Error during API request for {file_name}: {e}")
            time.sleep(retry_delay * (attempt + 1))
    return None

# ประมวลผลไฟล์และเก็บค่าที่ได้จาก API
def process_images():
    lp_numbers = []
    file_lp_mapping = {}
    processed_files = set()
    last_check_time = time.time()

    while True:
        for file_name in os.listdir(folder_path):
            if file_name.endswith((".jpg", ".png")) and file_name not in processed_files:
                file_path = os.path.join(folder_path, file_name)
                lp_number = send_image_to_api(file_path, file_name)

                if lp_number:
                    lp_numbers.append(lp_number)
                    file_lp_mapping[file_name] = lp_number
                    print(f"Processed {file_name}: lp_number = {lp_number}")
                else:
                    print(f"Failed to process {file_name}")

                processed_files.add(file_name)
                time.sleep(3)  # หน่วงเวลาเพื่อไม่ให้ส่ง API มากเกินไป

        current_time = time.time()
        if current_time - last_check_time >= 60:  # เช็คข้อมูลกับฐานข้อมูลทุก 1 นาที
            db_license_plates = get_license_plates_from_db()
            found_plates = check_lp_numbers_against_db(lp_numbers, db_license_plates)

            print(f"License plates found in database: {found_plates}")

            # ค้นหาการตรวจจับที่ตรงกับป้ายทะเบียนในฐานข้อมูล
            detections = {}
            for file_name, lp_number in file_lp_mapping.items():
                if lp_number in found_plates:
                    # เก็บเฉพาะข้อมูลสุดท้ายของแต่ละป้ายทะเบียนที่ซ้ำกัน
                    detections[lp_number] = file_name

            # ย้ายไฟล์ที่ตรวจจับได้เฉพาะไฟล์สุดท้ายของป้ายทะเบียนนั้นๆ
            for lp_number, file_name in detections.items():
                src_path = os.path.join(folder_path, file_name)
                dst_path = os.path.join(destination_folder, file_name)
                shutil.move(src_path, dst_path)
                print(f"Moved {file_name} to {destination_folder}")

            # บันทึกข้อมูลการตรวจจับลงในฐานข้อมูล
            insert_detection_records({file_name: lp_number for lp_number, file_name in detections.items()}, found_plates)

            # เคลียร์ค่าชั่วคราว
            lp_numbers.clear()
            file_lp_mapping.clear()

            # อัปเดตตัวจับเวลา
            last_check_time = current_time

        time.sleep(5)  # รอเพื่อวนรอบใหม่

# เริ่มการประมวลผล
process_images()
