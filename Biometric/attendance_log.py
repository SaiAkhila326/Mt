import os
import csv
import math
import sqlite3
import time
import random
import threading
import requests
from datetime import datetime
from io import StringIO

CSV_FILE = 'attendance_logs.csv'
DB_FILE = 'employee_database.db'
API_URL = 'https://yourserver.com/api/attendance'

UPLOAD_INTERVAL = 60  # seconds
SYNC_THRESHOLD = 5    # number of new rows before triggering upload

sync_lock = threading.Lock()
unsynced_rows = []  # Buffer to track unsynced rows


# Simulated biometric authentication
def simulate_iris_match(): return True
def simulate_face_match(): return random.choice([True, False])
def simulate_fingerprint_match(): return random.choice([True, False])


def is_within_radius(lat1, lon1, lat2, lon2, radius_m=20):
    R = 6371000  # Earth radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c  # Calculate actual distance

    # Debugging prints to verify values
    #print(f"DB Coordinates: {lat2}, {lon2}")
    #print(f"Scanned Coordinates: {lat1}, {lon1}")
    #print(f"Calculated Distance: {distance} meters")
    
    return distance <= radius_m  # Proper comparison


def authenticate_with_priority(max_attempts=10):
    for attempt in range(1, max_attempts + 1):
        if simulate_iris_match():
            return "Iris"
        if simulate_face_match():
            return "Face"
        if simulate_fingerprint_match():
            return "Fingerprint"
        time.sleep(0.5)
    return None


def write_to_csv(row):
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def upload_csv_rows(rows):
    if not rows:
        return

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
    csv_payload = output.getvalue()

    try:
        response = requests.post(API_URL, data=csv_payload, headers={'Content-Type': 'text/csv'})
        if response.status_code == 200:
            print(f" Uploaded {len(rows)} row(s) to API successfully.")
        else:
            print(f" Upload failed with status {response.status_code}")
    except Exception as e:
        print(f" Upload failed: {e}")


def periodic_sync():
    while True:
        time.sleep(UPLOAD_INTERVAL)
        with sync_lock:
            if unsynced_rows:
                upload_csv_rows(unsynced_rows.copy())
                unsynced_rows.clear()


def append_attendance_to_csv(emp_name, emp_id, curr_lat, curr_lon):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT Latitude, Longitude FROM employee_data WHERE Employee_ID = ?", (emp_id,))
    result = c.fetchone()
    conn.close()

    if not result:
        print(f" No location registered for {emp_name}")
        return

    reg_lat, reg_lon = result
    loc_match = is_within_radius(curr_lat, curr_lon, reg_lat, reg_lon)
    auth_method = authenticate_with_priority()

    if not auth_method or not loc_match:
        print(f" Failed auth or location for {emp_name}")
        return

    timestamp = datetime.now().isoformat()
    row = {
        "Employee_name": emp_name,
        "Employee_ID": emp_id,
        "Authentication_Method": auth_method,
        "Location_match": str(loc_match),
        "Timestamp": timestamp
    }

    write_to_csv(row)

    with sync_lock:
        unsynced_rows.append(row)
        if len(unsynced_rows) >= SYNC_THRESHOLD:
            upload_csv_rows(unsynced_rows.copy())
            unsynced_rows.clear()

    print(f" Logged and buffered: {emp_name}")


def match_all_employees():
    scan_lat, scan_lon = 17.3851, 78.4868  # Simulated office location
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT Employee_name, Employee_ID FROM employee_data")
    employees = c.fetchall()
    conn.close()

    for name, eid in employees:
        append_attendance_to_csv(name, eid, scan_lat, scan_lon)


if __name__ == "__main__":
    # Start periodic sync thread
    threading.Thread(target=periodic_sync, daemon=True).start()

    # Simulate scan for all employees
    match_all_employees()

    # Give time for async sync if script ends quickly
    time.sleep(5)

