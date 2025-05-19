import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.colors import LinearSegmentedColormap

# Load and clean
df = pd.read_csv('/usr/app/babysleepcoach/sleep_logs.csv', skiprows=1, names=['awake', 'timestamp'])
df = df[df['timestamp'].apply(lambda x: str(x).isdigit())]
df['timestamp'] = df['timestamp'].astype(int)
df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
# Filter to last 30 days
now = datetime.now()
month_ago = now - timedelta(days=30)
df = df[df['datetime'] >= month_ago]
# Track how often baby was asleep at each minute of the day
minutes_per_day = 24 * 60
sleep_minutes = np.zeros(minutes_per_day)

# Go through each sleep session (0 → 1)
for i in range(len(df) - 1):
    row = df.iloc[i]
    next_row = df.iloc[i + 1]

    if row.awake == 0 and next_row.awake == 1:
        start = row.datetime
        end = next_row.datetime

        # Loop over every minute in this sleep window
        t = start
        while t < end:
            minute_of_day = t.hour * 60 + t.minute
            sleep_minutes[minute_of_day] += 1
            t += timedelta(minutes=1)
# Normalize to 0–1 range (where 1 = slept every day at that minute)
sleep_minutes /= sleep_minutes.max()

# Custom colormap: dark blue (asleep) to yellow (awake)
sleep_cmap = LinearSegmentedColormap.from_list("sleep_awake", ["#FFFF00", "#000080"])  # navy to yellow

# Plot: 1 pixel high, 1440 pixels wide
plt.figure(figsize=(12, 1))
plt.imshow([sleep_minutes], cmap=sleep_cmap, aspect='auto')  # <-- sleep_minutes instead of 1 - sleep_minutes
plt.yticks([])  # Hide y-axis
plt.xticks(
    ticks=np.arange(0, 1441, 60),
    labels=[f"{h}:00" for h in range(25)],
    fontsize=8
)
plt.savefig("/usr/app/babysleepcoach/heatmap.png", bbox_inches='tight', pad_inches=0.1, dpi=300)
plt.close()
