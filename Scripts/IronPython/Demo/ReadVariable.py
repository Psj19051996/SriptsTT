# encoding:utf-8
from __future__ import print_function
import clr  # Import Common Language Runtime (CLR) for .NET support
import sys


# Add CODESYS Automation DLL path
sys.path.append(r"C:\Program Files (x86)\3S CODESYS\CODESYS 3.5 SP11\CODESYS\ScriptLib\3.5.10.40")

# Load CODESYS Automation Libraries
clr.AddReference("CODESYS.Automation")
clr.AddReference("CODESYS.Base")

# Now import required modules
from CODESYS.Automation import *

# ✅ Now the 'projects' object should work correctly
if projects.primary:
    projects.primary.close()

try:
    # Open the CODESYS project
    proj = projects.open(r"C:\Git\github.com\TribeTech_Group\TTDS_RC_FunctionDev\devices\tcp_ip\PF_RFID_Testing_PSJ.project")

    # Get the active application
    app = proj.active_application
    onlineapp = online.create_online_application(app)

    # Log in to the device
    onlineapp.login(OnlineChangeOption.Try, True)

    # Ensure the application is running
    if not onlineapp.application_state == ApplicationState.run:
        onlineapp.start()

    # Wait for 1 second
    system.delay(1000)

    # Read a variable value from the PLC
    value = onlineapp.read_value("PLC_PRG.xResetPLC")
    print("Value read from PLC:", value)

    # ✅ Log out from the device **only if logged in**
    if onlineapp.is_online:
        onlineapp.logout()
        print("Logged out successfully.")

except Exception as e:
    print("Error:", e)

finally:
    # Close the project
    if proj:
        proj.close()
        print("Project closed.")
