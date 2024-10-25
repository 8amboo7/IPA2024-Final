from netmiko import ConnectHandler
import re

def gigabit_status():
    device = {
        'device_type': 'cisco_ios',
        'host': '10.0.15.184',
        'username': 'admin',
        'password': 'cisco',
        # 'port': 22,
    }
    
    net_connect = ConnectHandler(**device)
    net_connect.enable()
    
    # ใช้คำสั่ง show interfaces status เพื่อดึงข้อมูลสถานะ
    output = net_connect.send_command("show ip interface brief")
    
    # เก็บสถานะของแต่ละอินเตอร์เฟซ GigabitEthernet
    interface_status = {}
    for line in output.splitlines():
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

        if status == "up":
            status_message.append(f"{interface} up")
            up_count += 1
        elif status == "down":
            status_message.append(f"{interface} down")
            down_count += 1
        elif "administratively down" in status:
            status_message.append(f"{interface} administratively down")
            admin_down_count += 1

    result_message = ", ".join(status_message) + f" -> {up_count} up, {down_count} down, {admin_down_count} administratively down"
    
    net_connect.disconnect()
    return result_message
