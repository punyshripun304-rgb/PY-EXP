import sqlite3
from datetime import datetime

DB_NAME = "mediflow.db"


def connect():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():
    with connect() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL CHECK(age >= 0),
            gender TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT DEFAULT '',
            registered_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            phone TEXT DEFAULT '',
            consultation_fee REAL NOT NULL CHECK(consultation_fee >= 0)
        );

        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL REFERENCES patients(id),
            doctor_id INTEGER NOT NULL REFERENCES doctors(id),
            appointment_at TEXT NOT NULL,
            reason TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'Scheduled'
                CHECK(status IN ('Scheduled', 'Completed', 'Cancelled'))
        );

        CREATE TABLE IF NOT EXISTS medical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL REFERENCES patients(id),
            doctor_id INTEGER NOT NULL REFERENCES doctors(id),
            appointment_id INTEGER REFERENCES appointments(id),
            diagnosis TEXT NOT NULL,
            treatment TEXT DEFAULT '',
            prescription TEXT DEFAULT '',
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            quantity INTEGER NOT NULL DEFAULT 0 CHECK(quantity >= 0),
            unit_price REAL NOT NULL CHECK(unit_price >= 0)
        );

        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL REFERENCES patients(id),
            appointment_id INTEGER REFERENCES appointments(id),
            consultation_charge REAL NOT NULL DEFAULT 0,
            medicine_charge REAL NOT NULL DEFAULT 0,
            other_charge REAL NOT NULL DEFAULT 0,
            total REAL NOT NULL,
            amount_paid REAL NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'Unpaid'
                CHECK(status IN ('Unpaid', 'Partially Paid', 'Paid')),
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS bill_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_id INTEGER NOT NULL REFERENCES bills(id) ON DELETE CASCADE,
            medicine_id INTEGER NOT NULL REFERENCES medicines(id),
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            unit_price REAL NOT NULL,
            subtotal REAL NOT NULL
        );
        """)


def read_int(prompt, minimum=0):
    while True:
        try:
            value = int(input(prompt).strip())
            if value < minimum:
                print(f"Enter a number greater than or equal to {minimum}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number.")


def read_float(prompt, minimum=0.0):
    while True:
        try:
            value = float(input(prompt).strip())
            if value < minimum:
                print(f"Enter a value greater than or equal to {minimum}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def read_required(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def choose_record(table, label):
    with connect() as conn:
        rows = conn.execute(f"SELECT * FROM {table} ORDER BY id").fetchall()
    if not rows:
        print(f"No {label.lower()} found. Add one first.")
        return None
    for row in rows:
        if table == "patients":
            print(f"{row['id']}: {row['name']} | Age {row['age']} | {row['phone']}")
        elif table == "doctors":
            print(f"{row['id']}: Dr. {row['name']} | {row['specialization']} | Fee ₹{row['consultation_fee']:.2f}")
        elif table == "appointments":
            print(f"{row['id']}: Patient #{row['patient_id']} with Doctor #{row['doctor_id']} | "
                  f"{row['appointment_at']} | {row['status']}")
        elif table == "medicines":
            print(f"{row['id']}: {row['name']} | Stock {row['quantity']} | ₹{row['unit_price']:.2f} each")
        elif table == "bills":
            print(f"{row['id']}: Patient #{row['patient_id']} | Total ₹{row['total']:.2f} | "
                  f"Due ₹{row['total'] - row['amount_paid']:.2f} | {row['status']}")
    return rows


def register_patient():
    print("\n--- Register Patient ---")
    name = read_required("Full name: ")
    age = read_int("Age: ")
    gender = read_required("Gender: ")
    phone = read_required("Phone: ")
    address = input("Address (optional): ").strip()
    with connect() as conn:
        cur = conn.execute(
            "INSERT INTO patients (name, age, gender, phone, address, registered_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (name, age, gender, phone, address, datetime.now().isoformat(timespec="minutes"))
        )
        print(f"Patient registered successfully. Patient ID: {cur.lastrowid}")


def list_patients():
    with connect() as conn:
        rows = conn.execute("SELECT * FROM patients ORDER BY id DESC").fetchall()
    print("\n--- Patients ---")
    if not rows:
        print("No patients registered.")
        return
    for r in rows:
        print(f"ID {r['id']} | {r['name']} | Age {r['age']} | {r['gender']} | "
              f"Phone {r['phone']} | Registered {r['registered_at']}")


def add_doctor():
    print("\n--- Add Doctor ---")
    name = read_required("Doctor name: ")
    specialization = read_required("Specialization: ")
    phone = input("Phone (optional): ").strip()
    fee = read_float("Consultation fee (₹): ")
    with connect() as conn:
        cur = conn.execute(
            "INSERT INTO doctors (name, specialization, phone, consultation_fee) VALUES (?, ?, ?, ?)",
            (name, specialization, phone, fee)
        )
        print(f"Doctor added successfully. Doctor ID: {cur.lastrowid}")


def list_doctors():
    with connect() as conn:
        rows = conn.execute("SELECT * FROM doctors ORDER BY id").fetchall()
    print("\n--- Doctors ---")
    if not rows:
        print("No doctors added.")
        return
    for r in rows:
        print(f"ID {r['id']} | Dr. {r['name']} | {r['specialization']} | "
              f"Phone {r['phone'] or '-'} | Fee ₹{r['consultation_fee']:.2f}")


def book_appointment():
    print("\n--- Book Appointment ---")
    print("Patients:")
    if choose_record("patients", "patients") is None:
        return
    patient_id = read_int("Patient ID: ", 1)
    print("Doctors:")
    if choose_record("doctors", "doctors") is None:
        return
    doctor_id = read_int("Doctor ID: ", 1)
    appointment_at = read_required("Appointment date/time (e.g. 2026-10-15 10:30): ")
    reason = input("Reason for visit (optional): ").strip()

    with connect() as conn:
        patient = conn.execute("SELECT id FROM patients WHERE id=?", (patient_id,)).fetchone()
        doctor = conn.execute("SELECT id FROM doctors WHERE id=?", (doctor_id,)).fetchone()
        if not patient or not doctor:
            print("Invalid patient or doctor ID.")
            return
        cur = conn.execute(
            "INSERT INTO appointments (patient_id, doctor_id, appointment_at, reason) "
            "VALUES (?, ?, ?, ?)",
            (patient_id, doctor_id, appointment_at, reason)
        )
        print(f"Appointment booked. Appointment ID: {cur.lastrowid}")


def list_appointments():
    with connect() as conn:
        rows = conn.execute("""
            SELECT a.*, p.name AS patient_name, d.name AS doctor_name
            FROM appointments a
            JOIN patients p ON p.id=a.patient_id
            JOIN doctors d ON d.id=a.doctor_id
            ORDER BY a.appointment_at
        """).fetchall()
    print("\n--- Appointments ---")
    if not rows:
        print("No appointments found.")
        return
    for r in rows:
        print(f"ID {r['id']} | {r['appointment_at']} | Patient: {r['patient_name']} "
              f"| Doctor: Dr. {r['doctor_name']} | {r['status']} | Reason: {r['reason'] or '-'}")


def complete_consultation():
    print("\n--- Doctor Consultation / Medical Record ---")
    if choose_record("appointments", "appointments") is None:
        return
    appointment_id = read_int("Appointment ID to complete: ", 1)
    with connect() as conn:
        appt = conn.execute("""
            SELECT a.*, d.consultation_fee
            FROM appointments a JOIN doctors d ON d.id=a.doctor_id
            WHERE a.id=?
        """, (appointment_id,)).fetchone()
        if not appt:
            print("Appointment not found.")
            return
        if appt["status"] == "Cancelled":
            print("This appointment was cancelled and cannot be completed.")
            return
        diagnosis = read_required("Diagnosis: ")
        treatment = input("Treatment / advice: ").strip()
        prescription = input("Prescription (medicine names and directions): ").strip()
        conn.execute("""
            INSERT INTO medical_records
            (patient_id, doctor_id, appointment_id, diagnosis, treatment, prescription, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (appt["patient_id"], appt["doctor_id"], appointment_id, diagnosis,
              treatment, prescription, datetime.now().isoformat(timespec="minutes")))
        conn.execute("UPDATE appointments SET status='Completed' WHERE id=?", (appointment_id,))
        print("Consultation saved and appointment marked completed.")
        print(f"Suggested consultation charge: ₹{appt['consultation_fee']:.2f}")


def view_medical_records():
    print("\n--- Medical Records ---")
    patient_id = read_int("Patient ID (enter 0 to view all): ", 0)
    with connect() as conn:
        if patient_id == 0:
            rows = conn.execute("""
                SELECT m.*, p.name AS patient_name, d.name AS doctor_name
                FROM medical_records m
                JOIN patients p ON p.id=m.patient_id
                JOIN doctors d ON d.id=m.doctor_id
                ORDER BY m.id DESC
            """).fetchall()
        else:
            rows = conn.execute("""
                SELECT m.*, p.name AS patient_name, d.name AS doctor_name
                FROM medical_records m
                JOIN patients p ON p.id=m.patient_id
                JOIN doctors d ON d.id=m.doctor_id
                WHERE m.patient_id=? ORDER BY m.id DESC
            """, (patient_id,)).fetchall()
    if not rows:
        print("No medical records found.")
        return
    for r in rows:
        print(f"\nRecord #{r['id']} | Patient: {r['patient_name']} | Doctor: Dr. {r['doctor_name']}")
        print(f"Date: {r['created_at']} | Diagnosis: {r['diagnosis']}")
        print(f"Treatment: {r['treatment'] or '-'}")
        print(f"Prescription: {r['prescription'] or '-'}")


def add_medicine():
    print("\n--- Add / Restock Medicine ---")
    name = read_required("Medicine name: ")
    quantity = read_int("Quantity to add: ", 1)
    price = read_float("Unit price (₹): ")
    with connect() as conn:
        existing = conn.execute("SELECT * FROM medicines WHERE name=?", (name,)).fetchone()
        if existing:
            conn.execute("UPDATE medicines SET quantity=quantity+?, unit_price=? WHERE id=?",
                         (quantity, price, existing["id"]))
            print(f"Stock updated. Current quantity: {existing['quantity'] + quantity}")
        else:
            cur = conn.execute("INSERT INTO medicines (name, quantity, unit_price) VALUES (?, ?, ?)",
                               (name, quantity, price))
            print(f"Medicine added. Medicine ID: {cur.lastrowid}")


def list_medicines():
    with connect() as conn:
        rows = conn.execute("SELECT * FROM medicines ORDER BY name").fetchall()
    print("\n--- Pharmacy Inventory ---")
    if not rows:
        print("No medicines in inventory.")
        return
    for r in rows:
        print(f"ID {r['id']} | {r['name']} | Stock: {r['quantity']} | Unit price: ₹{r['unit_price']:.2f}")


def create_bill():
    print("\n--- Create Patient Bill ---")
    if choose_record("patients", "patients") is None:
        return
    patient_id = read_int("Patient ID: ", 1)
    with connect() as conn:
        patient = conn.execute("SELECT id FROM patients WHERE id=?", (patient_id,)).fetchone()
        if not patient:
            print("Patient not found.")
            return
        appointments = conn.execute("""
            SELECT a.id, a.appointment_at, a.status, d.consultation_fee
            FROM appointments a JOIN doctors d ON d.id=a.doctor_id
            WHERE a.patient_id=? AND a.status='Completed'
            ORDER BY a.id DESC
        """, (patient_id,)).fetchall()
        if appointments:
            print("Completed appointments:")
            for a in appointments:
                print(f"ID {a['id']} | {a['appointment_at']} | Consultation ₹{a['consultation_fee']:.2f}")
            appointment_id = read_int("Appointment ID to bill (0 for none): ", 0)
        else:
            print("No completed appointments for this patient.")
            appointment_id = 0

        consultation_charge = 0.0
        if appointment_id:
            appt = conn.execute("""
                SELECT d.consultation_fee FROM appointments a
                JOIN doctors d ON d.id=a.doctor_id
                WHERE a.id=? AND a.patient_id=? AND a.status='Completed'
            """, (appointment_id, patient_id)).fetchone()
            if not appt:
                print("That appointment does not belong to this patient or is not completed.")
                return
            consultation_charge = float(appt["consultation_fee"])

        medicine_charge = 0.0
        bill_items = []
        while input("Add a medicine to this bill? (y/n): ").strip().lower() == "y":
            medicines = conn.execute("SELECT * FROM medicines ORDER BY name").fetchall()
            if not medicines:
                print("No medicines available. Add inventory first.")
                break
            for m in medicines:
                print(f"ID {m['id']} | {m['name']} | Stock {m['quantity']} | ₹{m['unit_price']:.2f}")
            medicine_id = read_int("Medicine ID (0 to stop): ", 0)
            if medicine_id == 0:
                break
            med = conn.execute("SELECT * FROM medicines WHERE id=?", (medicine_id,)).fetchone()
            if not med:
                print("Medicine not found.")
                continue
            quantity = read_int("Quantity: ", 1)
            already = sum(item[1] for item in bill_items if item[0] == medicine_id)
            if quantity + already > med["quantity"]:
                print("Not enough stock available.")
                continue
            bill_items.append((medicine_id, quantity, float(med["unit_price"])))
            medicine_charge += quantity * float(med["unit_price"])

        other_charge = read_float("Other charges (₹, enter 0 if none): ")
        total = consultation_charge + medicine_charge + other_charge
        cur = conn.execute("""
            INSERT INTO bills
            (patient_id, appointment_id, consultation_charge, medicine_charge, other_charge,
             total, amount_paid, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, 0, 'Unpaid', ?)
        """, (patient_id, appointment_id or None, consultation_charge, medicine_charge,
              other_charge, total, datetime.now().isoformat(timespec="minutes")))
        bill_id = cur.lastrowid

        for medicine_id, quantity, unit_price in bill_items:
            subtotal = quantity * unit_price
            conn.execute("""
                INSERT INTO bill_items (bill_id, medicine_id, quantity, unit_price, subtotal)
                VALUES (?, ?, ?, ?, ?)
            """, (bill_id, medicine_id, quantity, unit_price, subtotal))
            conn.execute("UPDATE medicines SET quantity=quantity-? WHERE id=?",
                         (quantity, medicine_id))

        print(f"\nBill created successfully. Bill ID: {bill_id}")
        print(f"Consultation: ₹{consultation_charge:.2f}")
        print(f"Medicines:    ₹{medicine_charge:.2f}")
        print(f"Other:        ₹{other_charge:.2f}")
        print(f"TOTAL:        ₹{total:.2f}")


def record_payment():
    print("\n--- Record Payment ---")
    if choose_record("bills", "bills") is None:
        return
    bill_id = read_int("Bill ID: ", 1)
    with connect() as conn:
        bill = conn.execute("SELECT * FROM bills WHERE id=?", (bill_id,)).fetchone()
        if not bill:
            print("Bill not found.")
            return
        due = round(float(bill["total"]) - float(bill["amount_paid"]), 2)
        if due <= 0:
            print("This bill is already paid.")
            return
        print(f"Outstanding amount: ₹{due:.2f}")
        amount = read_float("Payment amount (₹): ", 0.01)
        if amount > due:
            print("Payment cannot exceed the outstanding amount.")
            return
        paid = round(float(bill["amount_paid"]) + amount, 2)
        status = "Paid" if paid >= float(bill["total"]) else "Partially Paid"
        conn.execute("UPDATE bills SET amount_paid=?, status=? WHERE id=?",
                     (paid, status, bill_id))
        print(f"Payment recorded. Remaining due: ₹{float(bill['total']) - paid:.2f}")
        print(f"Bill status: {status}")


def list_bills():
    with connect() as conn:
        rows = conn.execute("""
            SELECT b.*, p.name AS patient_name
            FROM bills b JOIN patients p ON p.id=b.patient_id
            ORDER BY b.id DESC
        """).fetchall()
    print("\n--- Bills ---")
    if not rows:
        print("No bills found.")
        return
    for r in rows:
        due = float(r["total"]) - float(r["amount_paid"])
        print(f"Bill #{r['id']} | {r['patient_name']} | Date {r['created_at']} | "
              f"Total ₹{r['total']:.2f} | Paid ₹{r['amount_paid']:.2f} | "
              f"Due ₹{due:.2f} | {r['status']}")


def reports():
    print("\n--- MediFlow Summary Report ---")
    with connect() as conn:
        counts = {
            "Patients": conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0],
            "Doctors": conn.execute("SELECT COUNT(*) FROM doctors").fetchone()[0],
            "Appointments": conn.execute("SELECT COUNT(*) FROM appointments").fetchone()[0],
            "Completed consultations": conn.execute(
                "SELECT COUNT(*) FROM appointments WHERE status='Completed'").fetchone()[0],
            "Medical records": conn.execute("SELECT COUNT(*) FROM medical_records").fetchone()[0],
            "Medicines in catalogue": conn.execute("SELECT COUNT(*) FROM medicines").fetchone()[0],
            "Bills": conn.execute("SELECT COUNT(*) FROM bills").fetchone()[0],
        }
        total_billed = conn.execute("SELECT COALESCE(SUM(total),0) FROM bills").fetchone()[0]
        total_paid = conn.execute("SELECT COALESCE(SUM(amount_paid),0) FROM bills").fetchone()[0]
        low_stock = conn.execute("SELECT name, quantity FROM medicines WHERE quantity <= 5 ORDER BY quantity").fetchall()
    for label, count in counts.items():
        print(f"{label}: {count}")
    print(f"Total billed: ₹{total_billed:.2f}")
    print(f"Payments received: ₹{total_paid:.2f}")
    print(f"Outstanding balance: ₹{total_billed - total_paid:.2f}")
    print("\nLow-stock medicines (5 units or fewer):")
    if low_stock:
        for m in low_stock:
            print(f"- {m['name']}: {m['quantity']} units")
    else:
        print("None")


def main():
    initialize_database()
    actions = {
        "1": register_patient,
        "2": list_patients,
        "3": add_doctor,
        "4": list_doctors,
        "5": book_appointment,
        "6": list_appointments,
        "7": complete_consultation,
        "8": view_medical_records,
        "9": add_medicine,
        "10": list_medicines,
        "11": create_bill,
        "12": record_payment,
        "13": list_bills,
        "14": reports,
    }
    while True:
        print("""
========== MediFlow Hospital Management System ==========
 1. Register patient
 2. View patients
 3. Add doctor
 4. View doctors
 5. Book appointment
 6. View appointments
 7. Complete consultation / add medical record
 8. View medical records
 9. Add or restock medicine
10. View pharmacy inventory
11. Create patient bill
12. Record payment
13. View bills
14. Generate hospital summary report
 0. Exit
=========================================================
""")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Thank you for using MediFlow.")
            break
        action = actions.get(choice)
        if action:
            try:
                action()
            except sqlite3.IntegrityError as exc:
                print(f"Database validation error: {exc}")
            except sqlite3.Error as exc:
                print(f"Database error: {exc}")
            except (EOFError, KeyboardInterrupt):
                print("\nOperation cancelled.")
        else:
            print("Invalid option. Please choose a number from 0 to 14.")


if __name__ == "__main__":
    main()
