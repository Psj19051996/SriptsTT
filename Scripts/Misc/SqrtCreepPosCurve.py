import numpy as np
import matplotlib.pyplot as plt

# Parameters
rTargetSetpoint = 500.0  # Target position
rCurrentValue = np.linspace(0, 600, 500)  # Simulated LVDT positions
rRampSetpoint = 50.0  # Ramp range (50 mm)
rCreepSetpoint = 10.0  # Creep range (10 mm)
rErrorTol = 1.0  # Error tolerance
rMinFlow = 0.0  # Minimum flow
rMaxFlow = 80.0  # Maximum flow

# Arrays to store results
flow_setpoints = []

# Calculate flow setpoint for each position
for value in rCurrentValue:
    # Determine polarity and calculate ramp/creep start points
    if rTargetSetpoint >= value:
        # Positive polarity
        rRampStartLVDT = rTargetSetpoint - rRampSetpoint
        rCreepStartLVDT = rTargetSetpoint - rCreepSetpoint
    else:
        # Negative polarity
        rRampStartLVDT = rTargetSetpoint + rRampSetpoint
        rCreepStartLVDT = rTargetSetpoint + rCreepSetpoint

    # Logic to determine flow
    if abs(rTargetSetpoint - value) <= rErrorTol:
        # Target reached
        flow_setpoint = 0.0
    elif (rTargetSetpoint >= value and value >= rCreepStartLVDT) or \
         (rTargetSetpoint < value and value <= rCreepStartLVDT):
        # In creep zone
        flow_setpoint = rMinFlow
    elif (rTargetSetpoint >= value and value >= rRampStartLVDT) or \
         (rTargetSetpoint < value and value <= rRampStartLVDT):
        # In ramp zone
        rErrorMap = rCreepStartLVDT - value
        rNormalizedError = abs(rErrorMap / (rCreepStartLVDT - rRampStartLVDT))
        flow_setpoint = rMinFlow + (rMaxFlow - rMinFlow) * np.sqrt(rNormalizedError)
    else:
        # Before ramp or after creep zone
        flow_setpoint = rMaxFlow

    flow_setpoints.append(flow_setpoint)

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(rCurrentValue, flow_setpoints, label="Flow Setpoint", color="b", linewidth=2)
plt.axvline(rTargetSetpoint - rCreepSetpoint, color="orange", linestyle="--", label="Creep Start")
plt.axvline(rTargetSetpoint - rRampSetpoint, color="green", linestyle="--", label="Ramp Start")
plt.axvline(rTargetSetpoint + rCreepSetpoint, color="orange", linestyle="--", label="Creep Start (Negative)", alpha=0.6)
plt.axvline(rTargetSetpoint + rRampSetpoint, color="green", linestyle="--", label="Ramp Start (Negative)", alpha=0.6)
plt.axhline(rMinFlow, color="purple", linestyle=":", label="Creep Flow (Min Flow)")
plt.axhline(rMaxFlow, color="red", linestyle=":", label="Max Flow")
plt.xlabel("LVDT Position (mm)")
plt.ylabel("Flow Setpoint")
plt.title("Flow Setpoint vs. LVDT Position with Polarity Handling")
plt.legend()
plt.grid(True)
plt.show()
