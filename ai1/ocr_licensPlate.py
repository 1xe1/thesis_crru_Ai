import os
import time
import requests
import mysql.connector
from mysql.connector import pooling
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from threading import Thread

# ตั้งค่าโฟลเดอร์ที่มีไฟล์รูป
folder_path = "licensePlateFound"
destination_folder = "StudentWithoutHelmet"

# ตรวจสอบว่ามีโฟลเดอร์ปลายทางหรือไม่ ถ้าไม่มีก็สร้างใหม่
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# API URL และ header
url = "https://api.iapp.co.th/license-plate-recognition/file"
headers = {
    'apikey': 'yZH8V3McJdEX5PN560yxZeOhiCCVFzLm'
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

def check_lp_numbers_against_db(lp_numbers, db_license_plates):
    found_plates = {lp: db_license_plates[lp] for lp in lp_numbers if lp in db_license_plates}
    return found_plates

def insert_detection_records(detections):
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT MAX(DetectionID) FROM helmetdetection")
        max_id = cursor.fetchone()[0]
        new_id = (max_id + 1) if max_id is not None else 1

        now = datetime.now()
        for lp_number, data in detections.items():
            student_id = data['student_id']
            file_name = data['file_name']
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

def send_image_to_api(file_path, file_name):
    max_retries = 3
    retry_delay = 2
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

def start_gui():
    root = tk.Tk()
    root.title("Student Helmet Detection")
    root.geometry("800x600")
    root.configure(bg="#2e3b4e")

    style = ttk.Style()
    style.configure("TFrame", background="#2e3b4e")
    style.configure("TLabel", background="#2e3b4e", foreground="white", font=("Helvetica", 12))
    style.configure("TButton", background="#1f7a8c", foreground="white", font=("Helvetica", 12, "bold"))

    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(expand=True, fill="both")

    title_label = ttk.Label(main_frame, text="ระบบตรวจจับนักศึกษา", font=("Helvetica", 18, "bold"))
    title_label.pack(pady=10)

    result_frame = ttk.Frame(main_frame)
    result_frame.pack(pady=10, fill="both", expand=True)

    result_label = ttk.Label(result_frame, text="รหัสนักศึกษาและป้ายทะเบียนที่ตรวจพบ:")
    result_label.pack(anchor="w", padx=10)

    result_text = tk.Text(result_frame, height=15, width=70, wrap="word", bg="#f4f4f4", font=("Helvetica", 11), relief="groove")
    result_text.pack(side="left", fill="both", expand=True, padx=10)

    scrollbar = tk.Scrollbar(result_frame, command=result_text.yview)
    scrollbar.pack(side="right", fill="y")
    result_text.config(yscrollcommand=scrollbar.set)

    def update_gui(detections):
        result_text.delete("1.0", tk.END)
        for lp_number, data in detections.items():
            result_text.insert(tk.END, f"รหัสนักศึกษา: {data['student_id']}, ป้ายทะเบียน: {lp_number}\n")

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
                    time.sleep(3)

            current_time = time.time()
            if current_time - last_check_time >= 60:
                db_license_plates = get_license_plates_from_db()
                found_plates = check_lp_numbers_against_db(lp_numbers, db_license_plates)

                detections = {}
                for file_name, lp_number in file_lp_mapping.items():
                    if lp_number in found_plates:
                        detections[lp_number] = {
                            'student_id': found_plates[lp_number],
                            'file_name': file_name
                        }

                for lp_number, data in detections.items():
                    src_path = os.path.join(folder_path, data['file_name'])
                    dst_path = os.path.join(destination_folder, data['file_name'])
                    if os.path.exists(src_path):
                        try:
                            shutil.move(src_path, dst_path)
                            print(f"Moved {data['file_name']} to {destination_folder}")
                        except Exception as e:
                            print(f"Error moving {data['file_name']}: {e}")
                    else:
                        print(f"File not found: {src_path}")

                insert_detection_records(detections)
                update_gui(detections)
                lp_numbers.clear()
                file_lp_mapping.clear()
                last_check_time = current_time

            time.sleep(5)

    Thread(target=process_images, daemon=True).start()

    root.mainloop()

start_gui()
