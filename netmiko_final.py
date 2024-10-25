from netmiko import ConnectHandler
import re

def gigabit_status():
    device = {
        'device_type': 'cisco_ios',
        'host': '10.0.15.184',
        'username': 'admin',
        'password': 'cisco',
        'port': 22,
        'secret': 'your_enable_password',  # เพิ่มรหัสผ่านโหมด enable หากจำเป็น
    }
    
    net_connect = ConnectHandler(**device)
    net_connect.enable()
    
    # ใช้คำสั่ง show ip interface brief เพื่อดึงข้อมูลสถานะ
    output = net_connect.send_command("show ip interface brief")
    print(output)
    
    # เก็บสถานะของแต่ละอินเตอร์เฟซ GigabitEthernet
    interface_status = {}
    for line in output.splitlines():
        # แก้ไข regex ให้จับสถานะให้ตรงรูปแบบที่ได้รับ
        match = re.match(r'^(GigabitEthernet\d+)\s+\S+\s+\S+\s+\S+\s+(\S+)', line)
        if match:
            interface, status = match.groups()
            interface_status[interface] = status.lower()
    
    up_count = 0
    down_count = 0
    admin_down_count = 0
    status_message = []
    
    for interface, status in interface_status.items():
        # หลีกเลี่ยงการ shutdown GigabitEthernet1 ตามที่โจทย์ระบุ
        if interface == "GigabitEthernet1" and status != "up":
            status_message.append(f"{interface} up (not allowed to shutdown)")
            continue

        # ตรวจสอบสถานะและเพิ่มเข้าไปใน status_message ตามรูปแบบ
        if status == "up":
            status_message.append(f"{interface} up")
            up_count += 1
        elif status == "down":
            status_message.append(f"{interface} down")
            down_count += 1
        elif status == "administratively down":
            status_message.append(f"{interface} administratively down")
            admin_down_count += 1

    # สร้างข้อความผลลัพธ์ตามรูปแบบที่ต้องการ
    result_message = ", ".join(status_message) + f" -> {up_count} up, {down_count} down, {admin_down_count} administratively down"
    return result_message
    net_connect.disconnect()

