# setup_employee_db.py

import sqlite3

DB_FILE = 'employee_database.db'

def create_employee_database():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS employee_data (
            Employee_name TEXT,
            Employee_ID TEXT PRIMARY KEY,
            Latitude REAL,
            Longitude REAL,
            Fingerprint_template BLOB,
            Face_template BLOB,
            Iris_template BLOB
        )
    ''')
    conn.commit()
    conn.close()
    print(" Database created and ready!")

def insert_employee(emp_name, emp_id, lat, lon, fp_blob, face_blob, iris_blob):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO employee_data (
            Employee_name, Employee_ID, Latitude, Longitude,
            Fingerprint_template, Face_template, Iris_template
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (emp_name, emp_id, lat, lon, fp_blob, face_blob, iris_blob))
    conn.commit()
    conn.close()
    print(f" Registered: {emp_name} ({emp_id})")

if __name__ == "__main__":
    create_employee_database()

    # Add employees (dummy data with sample templates)
    insert_employee("Sri-ram Nulu", "E001", 17.3850, 78.4867, b'fp_data', b'face_data', b'iris_data')
    insert_employee("Sai-Akhila", "E002", 171.3850, 78.4867, b'fp_data', b'face_data', b'iris_data')
    insert_employee("Sarthak", "E003", 17.450, 79.4867, b'fp_data', b'face_data', b'iris_data')
    

