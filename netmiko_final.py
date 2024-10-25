from netmiko import ConnectHandler
import re

def gigabit_status():
    device = {
        'device_type': 'cisco_ios',
        'host': '10.0.15.184',
        'username': 'admin',
        'password': 'cisco',
        'port': 22,
        
        # 'secret': 'your_secret',  # ใช้ secret หากต้องการเข้าถึงโหมด enable
    }
    
    net_connect = ConnectHandler(**device)
    net_connect.enable()
    
    output = net_connect.send_command("show interfaces status", use_textfsm=True)
    
    interface_status = {}
    for interface in output:
        if re.match(r'^GigabitEthernet\d+', interface['port']):
            interface_status[interface['port']] = interface['status'].lower()
    
    up_count = 0
    down_count = 0
    admin_down_count = 0
    status_message = []
    
    for interface, status in interface_status.items():
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
