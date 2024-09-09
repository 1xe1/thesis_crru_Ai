from ultralytics import YOLO
import cv2
import os

# โหลดโมเดลที่ฝึกฝนแล้ว
model = YOLO(r'runs\detect\train\weights\best.pt')

# เปิดกล้อง
cap = cv2.VideoCapture(0)  # ใช้ 0 สำหรับกล้องหลัก

if not cap.isOpened():
    print("Error: Could not open video capture.")
    exit()

# สร้างโฟลเดอร์สำหรับบันทึกภาพถ้าไม่อยู่แล้ว
output_dir = 'save'
os.makedirs(output_dir, exist_ok=True)

frame_count = 0  # ตัวนับจำนวนเฟรม
confidence_threshold = 0.5  # ตั้งค่าความแม่นยำขั้นต่ำ
delay = 500  # หน่วงเวลา 500 มิลลิวินาที (0.5 วินาที)

while True:
    # อ่านภาพจากกล้อง
    ret, img = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # ทำการตรวจจับวัตถุ
    results = model(img)

    # ตรวจสอบว่ามีผลลัพธ์หรือไม่
    if results:
        # ดึงข้อมูลจาก results
        output_img = img.copy()
        
        # ตรวจสอบว่า results เป็น list หรือไม่
        if isinstance(results, list):
            result = results[0]  # เลือกผลลัพธ์แรก (ถ้ามีหลายภาพ)

            # เข้าถึงข้อมูล
            boxes = result.boxes.xyxy.cpu().numpy()  # พิกัดกรอบ
            confidences = result.boxes.conf.cpu().numpy()  # ความแม่นยำ
            class_ids = result.boxes.cls.cpu().numpy()  # ID ของคลาส
            names = result.names  # ชื่อของคลาส

            # ตรวจสอบวัตถุที่ต้องการ
            object_detected = False  # สถานะการตรวจจับวัตถุที่ต้องการ

            for i, box in enumerate(boxes):
                x1, y1, x2, y2 = map(int, box[:4])
                confidence = confidences[i]
                class_id = int(class_ids[i])
                label = names[class_id] if class_id < len(names) else 'Unknown'

                # ตรวจสอบสถานะการตรวจจับและความแม่นยำ
                if label in ['With Helmet', 'Without Helmet'] and confidence >= confidence_threshold:
                    object_detected = True
                    text = f"{label} {confidence:.2f}"  # ข้อความที่แสดงความแม่นยำ
                    cv2.rectangle(output_img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # วาดกรอบ
                    cv2.putText(output_img, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  # วาดข้อความ

            # ถ้าพบวัตถุที่ต้องการ, บันทึกภาพ
            if object_detected:
                frame_count += 1
                output_path = os.path.join(output_dir, f'detected_image_{frame_count}.jpg')
                cv2.imwrite(output_path, output_img)
                print(f"Saved: {output_path}")

    # หน่วงเวลา 0.5 วินาที
    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break

# ปิดกล้องและหน้าต่าง
cap.release()
cv2.destroyAllWindows()
