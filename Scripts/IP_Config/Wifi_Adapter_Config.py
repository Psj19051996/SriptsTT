import os
import sys
import ctypes
import subprocess
import time

def is_admin():
    """Checks if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"Error checking admin rights: {e}")
        return False

def elevate_to_admin():
    """Relaunches the script with administrative privileges."""
    try:
        script = os.path.abspath(sys.argv[0])
        params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
        sys.exit(0)  # Exit the current instance
    except Exception as e:
        print(f"Failed to elevate privileges: {e}")
        sys.exit(1)

def check_admin():
    """Ensures the script is running with administrative privileges."""
    if not is_admin():
        print("This script requires administrative privileges. Restarting with elevated permissions...")
        elevate_to_admin()

def get_connected_ssid():
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"],
            capture_output=True, text=True, check=True
        )
        for line in result.stdout.splitlines():
            if "SSID" in line and "BSSID" not in line:
                ssid = line.split(":")[1].strip()
                return ssid
    except subprocess.CalledProcessError as e:
        print(f"Failed to get connected SSID: {e}")
        return None

def set_static_ip_windows(interface_name, ip_address, subnet_mask, gateway):
    try:
        subprocess.run([
            "netsh", "interface", "ip", "set", "address",
            f"name={interface_name}", "static",
            ip_address, subnet_mask, gateway
        ], check=True)
        print(f"Static IP set to {ip_address} on {interface_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set static IP: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def set_dhcp_windows(interface_name):
    try:
        subprocess.run([
            "netsh", "interface", "ip", "set", "address",
            f"name={interface_name}", "dhcp"
        ], check=True)
        print(f"Adapter {interface_name} set to DHCP mode")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set DHCP: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def find_free_ips(base_ip="10.254.251.", start=20, end=50):
    free_ips = []
    for i in range(start, end + 1):
        ip = f"{base_ip}{i}"
        response = subprocess.run(["ping", "-n", "1", "-w", "100", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "Destination host unreachable" in response.stdout or "Request timed out" in response.stdout:
            free_ips.append(ip)
        else:
            print(f"{ip} is in use.")
    
    return free_ips  # Return the list of free IPs

def main():
    check_admin()  # Ensure script is running as admin

    interface_name = "Wi-Fi"  # Replace with your network adapter's name

    while True:
        connected_ssid = get_connected_ssid()
        ssid_list = ["TP-Link", "Rig", "Tel"] # changed to a list.
        if connected_ssid:
            print(f"Connected to SSID: {connected_ssid}")

            if any(connected_ssid.startswith(ssid) for ssid in ssid_list): # check if any of the ssid_list items match
                ip_address = "10.254.251.20"  # Use the first free IP
                subnet_mask = "255.255.255.0"  # Replace with your subnet mask
                gateway = ""  # Replace with your gateway if needed
                set_static_ip_windows(interface_name, ip_address, subnet_mask, gateway)
                print(f"Using free IP {ip_address} for static IP configuration.")
            else:
                set_dhcp_windows(interface_name)
                print("No matching SSID found; Set to DHCP by Default.")
        else:
            print("Could not detect a connected WiFi network.")
        
        time.sleep(2)  # Wait 1 second before repeating the check
        sys.exit(0)

if __name__ == "__main__":
    main()