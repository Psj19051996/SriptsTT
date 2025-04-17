import win32serviceutil
import win32service
import win32event
import servicemanager
import os
import sys
import ctypes
import subprocess
import time

class WifiConfigService(win32serviceutil.ServiceFramework):
    _svc_name_ = "WifiConfigService"
    _svc_display_name_ = "WiFi Configuration Service"
    _svc_description_ = "A service to configure WiFi adapter settings based on SSID."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.running = False
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, "")
        )
        self.main()

    def main(self):
        # Replace this loop with your main logic
        interface_name = "Wi-Fi"  # Replace with your network adapter's name
        last_ssid_processed = None

        while self.running:
            connected_ssid = self.get_connected_ssid()

            if connected_ssid:
                if connected_ssid != last_ssid_processed:
                    if connected_ssid == "iPhone (4)":
                        self.set_dhcp_windows(interface_name)
                        last_ssid_processed = connected_ssid
                    elif connected_ssid == "GL-MT3000-0a2-5G":
                        ip_address = "10.254.251.22"  # Replace with your desired IP address
                        subnet_mask = "255.255.255.0"  # Replace with your subnet mask
                        gateway = ""  # Replace with your gateway
                        self.set_static_ip_windows(interface_name, ip_address, subnet_mask, gateway)
                        last_ssid_processed = connected_ssid
                    else:
                        print("No matching SSID found; no changes applied.")
                else:
                    print("SSID already processed; no changes applied.")
            else:
                print("Could not detect a connected WiFi network.")

            time.sleep(1)  # Wait 1 second before repeating the check

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def get_connected_ssid(self):
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

    def set_static_ip_windows(self, interface_name, ip_address, subnet_mask, gateway):
        try:
            subprocess.run([
                "netsh", "interface", "ip", "set", "address",
                f"name={interface_name}", "static",
                ip_address, subnet_mask, gateway
            ], check=True)
            print(f"Static IP set to {ip_address} on {interface_name}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to set static IP: {e}")

    def set_dhcp_windows(self, interface_name):
        try:
            subprocess.run([
                "netsh", "interface", "ip", "set", "address",
                f"name={interface_name}", "dhcp"
            ], check=True)
            print(f"Adapter {interface_name} set to DHCP mode")
        except subprocess.CalledProcessError as e:
            print(f"Failed to set DHCP: {e}")

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(WifiConfigService)
