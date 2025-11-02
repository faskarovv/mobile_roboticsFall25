import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv('path_log.csv')
df.columns = df.columns.str.strip()  # remove extra spaces

# Extract columns
x = df['x_mm']
y = df['y_mm']
heading = df['heading_deg']
time = df['time_ms']

# Plot XY path
plt.figure(figsize=(8,6))
plt.plot(x, y, marker='.', linestyle='-', color='green')
plt.title('Robot Path')
plt.xlabel('X position (mm)')
plt.ylabel('Y position (mm)')
plt.axis('equal')
plt.grid(True)
plt.show()

# Plot heading over time
plt.figure(figsize=(8,4))
plt.plot(time, heading, color='red')
plt.title('Robot Heading over Time')
plt.xlabel('Time (ms)')
plt.ylabel('Heading (degrees)')
plt.grid(True)
plt.show()
