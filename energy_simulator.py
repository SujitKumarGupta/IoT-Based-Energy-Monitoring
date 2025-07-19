import os
import pandas as pd
import random
from datetime import datetime, timedelta

# Resolve path to the CSV file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "energy_data.csv")

# Ensure the 'data' directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# List of devices
devices = ["AC", "Computer", "Printer", "Projector"]

def simulate_data():
    # Current time
    now = datetime.now()

    # Try loading existing data
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=["timestamp", "device", "energy_usage"])
    else:
        df = pd.DataFrame(columns=["timestamp", "device", "energy_usage"])

    # Generate new entries (e.g., 6 new rows spaced by 10 minutes)
    new_entries = []
    for i in range(6):
        timestamp = now - timedelta(minutes=10 * i)
        device = random.choice(devices)
        energy_usage = round(random.uniform(0.2, 1.5), 2)  # kWh
        new_entries.append({
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "device": device,
            "energy_usage": energy_usage
        })

    # Append new entries and save
    df = pd.concat([df, pd.DataFrame(new_entries)], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    print("Energy data simulated and logged successfully.")

if __name__ == "__main__":
    simulate_data()
