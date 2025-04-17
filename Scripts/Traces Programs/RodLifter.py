import matplotlib.pyplot as plt

class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0

    def compute(self, error, dt):
        """Compute PID correction based on the error, making adjustments for better tuning."""
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.prev_error = error
        return output

def synchronize_cylinders(target1, target2, pos1, pos2, dt, pid):
    """Synchronize cylinders based on percentage progress."""
    perc1 = min(pos1 / target1, 1.0) if target1 != 0 else 0
    perc2 = min(pos2 / target2, 1.0) if target2 != 0 else 0
    
    error = perc1 - perc2  # Difference in progress
    correction = pid.compute(error, dt)

    # Adjusting velocity based on error size
    base_speed = 10.0
    extra_speed = abs(correction) * 5  # Higher error leads to larger speed correction

    if error > 0:  
        vel1 = base_speed
        vel2 = base_speed + extra_speed  # Increase speed of trailing cylinder
    else:
        vel1 = base_speed + extra_speed  
        vel2 = base_speed

    # Ensure velocity is within valid bounds
    vel1 = max(1.0, vel1)
    vel2 = max(1.0, vel2)

    return vel1, vel2, perc1, perc2

# Initialize PID Controller with Tuned Values
pid = PIDController(kp=2.0, ki=0.1, kd=0.5)  # More aggressive P and D tuning

# Targets for each cylinder
target1, target2 = 100, 150  # Different targets
pos1, pos2 = 0, 0  # Initial positions
dt = 0.1  # Time step

# Lists to store data for plotting
pos1_list, pos2_list = [], []
vel1_list, vel2_list = [], []
perc1_list, perc2_list = [], []

while pos1 < target1 or pos2 < target2:
    vel1, vel2, perc1, perc2 = synchronize_cylinders(target1, target2, pos1, pos2, dt, pid)

    # Update positions without exceeding targets
    if pos1 < target1:
        pos1 += vel1 * dt
    if pos2 < target2:
        pos2 += vel2 * dt

    # Ensure positions don't exceed their targets
    pos1 = min(pos1, target1)
    pos2 = min(pos2, target2)

    # Store data for plotting
    pos1_list.append(pos1)
    pos2_list.append(pos2)
    vel1_list.append(vel1)
    vel2_list.append(vel2)
    perc1_list.append(perc1)
    perc2_list.append(perc2)

    print(f"Positions: Cylinder1={pos1:.2f}, Cylinder2={pos2:.2f}, Vel1={vel1:.2f}, Vel2={vel2:.2f}, Perc1={perc1:.2f}, Perc2={perc2:.2f}")

print("Synchronization Complete")

# Plot Velocity vs. Position Graphs
plt.figure(figsize=(10, 5))

# Plot for Cylinder 1
plt.subplot(1, 2, 1)
plt.plot(pos1_list, vel1_list, label="Cylinder 1", color="blue")
plt.xlabel("Position")
plt.ylabel("Velocity")
plt.title("Velocity vs Position (Cylinder 1)")
plt.legend()
plt.grid()

# Plot for Cylinder 2
plt.subplot(1, 2, 2)
plt.plot(pos2_list, vel2_list, label="Cylinder 2", color="red")
plt.xlabel("Position")
plt.ylabel("Velocity")
plt.title("Velocity vs Position (Cylinder 2)")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
