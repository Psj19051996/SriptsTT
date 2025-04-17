import os
import sys
import ctypes
import subprocess
import logging

# Setup logging
LOG_FILE = "wifi_network_change.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def is_admin():
    """Checks if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        logging.error(f"Error checking admin rights: {e}")
        return False

def elevate_to_admin():
    """Relaunches the script with administrative privileges."""
    try:
        script = os.path.abspath(sys.argv[0])
        params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
        sys.exit(0)  # Exit the current instance
    except Exception as e:
        logging.error(f"Failed to elevate privileges: {e}")
        sys.exit(1)

def check_admin():
    """Ensures the script is running with administrative privileges."""
    if not is_admin():
        logging.info("Restarting with elevated permissions...")
        elevate_to_admin()

def get_connected_ssid():
    """Retrieves the currently connected WiFi SSID."""
    try:
        result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if "SSID" in line and "BSSID" not in line:
                ssid = line.split(":")[1].strip()
                return ssid
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to get connected SSID: {e}")
        return None

def set_static_ip_windows(interface_name, ip_address, subnet_mask, gateway=""):
    """Sets a static IP address on the given network interface."""
    try:
        subprocess.run([
            "netsh", "interface", "ip", "set", "address",
            f"name={interface_name}", "static",
            ip_address, subnet_mask, gateway
        ], check=True)
        logging.info(f"Static IP set to {ip_address} on {interface_name}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to set static IP: {e}")

def set_dhcp_windows(interface_name):
    """Sets the network adapter to use DHCP (automatic IP assignment)."""
    try:
        subprocess.run([
            "netsh", "interface", "ip", "set", "address",
            f"name={interface_name}", "dhcp"
        ], check=True)
        logging.info(f"Adapter {interface_name} set to DHCP mode")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to set DHCP: {e}")

def find_free_ips(base_ip="10.254.251.", start=20, end=35):
    """Finds free IPs within a given range by pinging them."""
    free_ips = []
    for i in range(start, end + 1):
        ip = f"{base_ip}{i}"
        response = subprocess.run(["ping", "-n", "1", "-w", "100", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "Destination host unreachable" in response.stdout or "Request timed out" in response.stdout:
            free_ips.append(ip)

    return free_ips  # Return list of free IPs

def main():
    check_admin()  # Ensure script is running as admin

    interface_name = "Wi-Fi"  # Adjust to match your network adapter's name
    #connected_ssid_ls = ["TP-Link_18E3_5G", "TP-Link_18E3", "TP-Link_F64E_5G", "Rig1_commissioning", "GL-MT3000-0a2-5G"]

    connected_ssid = get_connected_ssid()

    if connected_ssid:
        logging.info(f"Connected to SSID: {connected_ssid}")

        if connected_ssid.startswith("TP-Link"):
            # Find a free IP to use
            #free_ips = find_free_ips()
            ip_address = "10.254.251.40"  # Use the first free IP
            subnet_mask = "255.255.255.0"  # Replace with your subnet mask
            set_static_ip_windows(interface_name, ip_address, subnet_mask)
            logging.info(f"Using free IP {ip_address} for static IP configuration.")
        else:
            set_dhcp_windows(interface_name)
            logging.info("Set to DHCP by default.")
    else:
        logging.warning("Could not detect a connected WiFi network.")

    sys.exit(0)  # Exit after running once

if __name__ == "__main__":
    main()
