import subprocess
import requests
import os
from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN = os.getenv("API_token")
ROOM_ID = "Y2lzY29zcGFyazovL3VzL1JPT00vNTFmNTJiMjAtNWQwYi0xMWVmLWE5YTAtNzlkNTQ0ZjRkNGZi"  # ระบุ roomId ของ Webex Teams ที่ต้องการส่งข้อความไป
STUDENT_ID = "65070211"  # ระบุ studentID ของคุณ
ROUTER_NAME = "CSR1KV-Pod1-4"  # ระบุชื่อ router

def run_ansible_playbook():
    playbook_command = ["ansible-playbook", "playbook.yaml"]
    
    # รัน Ansible playbook ด้วย subprocess
    result = subprocess.run(playbook_command, capture_output=True, text=True)
    
    if result.returncode == 0:
        # ถ้า playbook ทำงานสำเร็จ ให้เตรียมส่งไฟล์
        filename = f"show_run_{STUDENT_ID}_{ROUTER_NAME}.txt"
        filepath = os.path.join(os.getcwd(), filename)
        
        if os.path.exists(filepath):
            send_file_to_webex(filepath)
        else:
            print("Error: File not found")
    else:
        # ถ้ามีข้อผิดพลาดใน playbook ส่งข้อความ "Error: Ansible" ไปที่ Webex Team room
        send_message_to_webex("Error: Ansible")

def send_file_to_webex(filepath):
    url = "https://webexapis.com/v1/messages"
    headers = {
        "Authorization": ACCESS_TOKEN,
        "Content-Type": "multipart/form-data"
    }
    with open(filepath, "rb") as file:
        files = {
            "roomId": (None, ROOM_ID),
            "text": (None, "Attached show running config file"),
            "files": (filepath, file, "text/plain")
        }
        response = requests.post(url, headers=headers, files=files)
        
        if response.status_code == 200:
            print("File sent successfully to Webex Teams")
        else:
            print(f"Error sending file: {response.status_code}")

def send_message_to_webex(message):
    url = "https://webexapis.com/v1/messages"
    headers = {
        "Authorization": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    data = {
        "roomId": ROOM_ID,
        "text": message
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("Message sent successfully to Webex Teams")
    else:
        print(f"Error sending message: {response.status_code}")

# เรียกใช้งานฟังก์ชันหลัก
run_ansible_playbook()
