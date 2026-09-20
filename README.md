# Hospital Management System

A menu-driven console application built in Python as part of the **Python Programming Lab – Experiential Learning Project**.

> **Current status: Utility Assessment – I (Initial Version, v0.1)**
> The Patient Management module is implemented and working. The remaining six modules are defined in the menu structure but are not yet implemented — they are honest placeholders that will be developed in later assessments.

---

## Problem Statement

Hospitals handle a large volume of day-to-day information: patient details, doctor availability, appointments, treatment records, bills and medicine stock. When this is maintained on paper or in scattered registers, the same data gets duplicated, records are hard to search, and generating any kind of summary takes a long time.

This project aims to build a single console-based system that stores and organises this information, so that a record can be entered once and then retrieved, searched and summarised reliably.

---

## Objectives

- Provide one entry point for all hospital record-keeping operations.
- Validate data at the point of entry so that invalid records never get stored.
- Keep each functional area in its own module so the system can grow in stages.
- Apply the Python concepts covered in the course: control structures, data structures, functions, file handling, NumPy/Pandas and OOP.

---

## Planned Modules

| # | Module | Purpose | Status |
|---|--------|---------|--------|
| 1 | Patient Management | Register, view and search patients | **Implemented** |
| 2 | Doctor Management | Doctor profiles, specialisation, availability | Planned |
| 3 | Appointment Management | Book and track patient–doctor appointments | Planned |
| 4 | Medical Records | Diagnosis and treatment history per patient | Planned |
| 5 | Billing | Consultation and treatment charges, invoices | Planned |
| 6 | Pharmacy | Medicine stock and dispensing | Planned |
| 7 | Reports | Summary statistics and analysis | Planned |

---

## Current Implementation (Assessment-I)

### What works
- Main menu loop with 8 options and validation of invalid choices.
- **Patient Management** sub-menu:
  - Register a new patient (ID, Name, Age, Gender, Contact Number)
  - View all registered patients in a formatted table
  - Search for a patient by Patient ID
- Input validation:
  - Blank fields are rejected
  - Age must be a whole number between 1 and 120
  - Gender accepts M / F / O and is normalised
  - Contact number must be exactly 10 digits
  - Duplicate Patient IDs are rejected
- The other six modules display a clear "not yet implemented" message and return to the main menu.

### What does not work yet (by design)
- Data is stored **in memory only** (a list of dictionaries) and is lost when the program exits. File handling arrives in Assessment-II.
- Modules 2–7 contain no logic yet.
- No classes/objects yet — the current version is function-based.

---

## Program Flow

```
START
  |
  v
Display Main Menu  <-------------------+
  |                                    |
  v                                    |
Read user choice (1-8)                 |
  |                                    |
  +-- 1 --> Patient Management sub-menu|
  |           |-- 1 Register patient   |
  |           |-- 2 View all patients  |
  |           |-- 3 Search patient     |
  |           +-- 4 Back --------------+
  |                                    |
  +-- 2..7 --> "Module not yet implemented"
  |                                    |
  +-- 8 --> Exit (break loop) --> END  |
  |                                    |
  +-- invalid --> Error message -------+
```

---

## Repository Structure

```
hospital-management-system/
├── hospital_management.py   # Main program (menu + all module functions)
├── README.md                # Project documentation (this file)
├── .gitignore               # Files excluded from version control
└── docs/
    ├── design.md            # Problem understanding, design decisions, roadmap
    └── viva_notes.md        # Preparation notes for the viva voce
```

---

## How to Run

Requires Python 3.6 or above. No external libraries are needed.

```bash
git clone https://github.com/<your-username>/hospital-management-system.git
cd hospital-management-system
python hospital_management.py
```

---

## Sample Output

```
==================================================
            HOSPITAL MANAGEMENT SYSTEM
==================================================
1. Patient Management
2. Doctor Management
3. Appointment Management
4. Medical Records
5. Billing
6. Pharmacy
7. Reports
8. Exit
==================================================
Enter your choice (1-8): 1

==================================================
                PATIENT MANAGEMENT
==================================================
  1. Register New Patient
  2. View All Patients
  3. Search Patient by ID
  4. Back to Main Menu
  ----------------------------------------------
  Enter your choice (1-4): 1

==================================================
               REGISTER NEW PATIENT
==================================================
  Enter Patient ID      : P101
  Enter Patient Name    : Rahul Sharma
  Enter Age             : 24
  Enter Gender (M/F/O)  : M
  Enter Contact Number  : 9876543210

  Patient registered successfully!
  ----------------------------------------
  Patient ID      : P101
  Name            : Rahul Sharma
  Age             : 24
  Gender          : Male
  Contact Number  : 9876543210
  ----------------------------------------
  Total patients registered: 1
```

---

## Python Concepts Used in This Version

| Concept | Where it is used |
|---------|------------------|
| Variables & data types | Patient fields, menu choices |
| Type conversion | `int(raw_age)` in `get_valid_age()` |
| `if / elif / else` | Menu dispatch, all validation |
| `while` loop | Main menu loop, sub-menu loop, re-prompting on bad input |
| `break` / `continue` | Exiting menus, skipping invalid input |
| `for` loop | Iterating over the patient list |
| Lists | `patients` list |
| Dictionaries | Each patient record |
| Functions / modularity | 15+ user-defined functions, one responsibility each |
| String methods | `.strip()`, `.upper()`, `.title()`, `.isdigit()`, `.format()` |

---

## Development Roadmap

| Stage | Planned work |
|-------|--------------|
| **Assessment-I (done)** | Menu structure, Patient Management, input validation, Git repo + README |
| Assessment-II | File handling (save/load patients to CSV or JSON), Doctor and Appointment modules |
| Assessment-III | Refactor into OOP (`Patient`, `Doctor`, `Appointment` classes), Medical Records, Billing |
| Assessment-IV | Pharmacy module, Reports using NumPy/Pandas, exception handling, final documentation |

---

## Author

3rd Year, B.Tech CSE (Data Science)
Python Programming Lab – Experiential Learning Project
