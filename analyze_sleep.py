import csv
import datetime
from pathlib import Path
def load_sleep_data(csv_path):
    rows = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "awake": int(row["awake"]),
                "timestamp": int(row["time"])
            })
    return rows

def to_sleep_sessions(rows):
    """Returner alle søvnøkter som (start, slutt)-par"""
    sessions = []
    for i in range(len(rows) - 1):
        cur = rows[i]
        nxt = rows[i + 1]
        if cur["awake"] == 0 and nxt["awake"] == 1:
            sessions.append((cur["timestamp"], nxt["timestamp"]))
    return sessions

def filter_last_month(sessions):
    now = datetime.datetime.now().timestamp()
    one_month_ago = now - (30 * 24 * 60 * 60)
    return [
        (start, end) for start, end in sessions
        if start >= one_month_ago
    ]

def average_sleep_duration(sessions):
    if not sessions:
        return 0
    durations = [end - start for start, end in sessions]
    return sum(durations) / len(durations)

def format_duration(seconds):
    minutes = seconds // 60
    hours = minutes // 60
    return f"{int(hours)}h {int(minutes % 60)}m"

if __name__ == "__main__":
    path = Path("/usr/app/babysleepcoach/sleep_logs.csv")
    rows = load_sleep_data(path)
    sessions = to_sleep_sessions(rows)
    recent_sessions = filter_last_month(sessions)
    avg_duration = int(average_sleep_duration(recent_sessions))

with open("/usr/app/babysleepcoach/monthly_sleep_stats.txt", "w", encoding="utf-8") as f:
    f.write(f"{avg_duration}")

