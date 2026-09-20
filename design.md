# Design Document — Hospital Management System

**Stage:** Utility Assessment – I (Initial Version)

---

## 1. Problem Understanding

A hospital records the same information many times in different places. A patient's name and contact go into an admission register, again into the doctor's file, again onto the bill, and again into the pharmacy slip. Three problems follow from this:

1. **Duplication and inconsistency** — the same patient exists in four registers with slightly different spellings, so nobody knows which record is correct.
2. **Slow retrieval** — finding one patient's treatment history means searching several physical registers by hand.
3. **No summary view** — questions like "how many patients did we see this month" require counting entries manually.

A software system solves this by storing each entity **once**, giving it a unique identifier, and linking the other records to that identifier.

---

## 2. Entities and Relationships

| Entity | Key field | Related to |
|--------|-----------|------------|
| Patient | Patient ID | Appointments, Medical Records, Bills |
| Doctor | Doctor ID | Appointments, Medical Records |
| Appointment | Appointment ID | Patient ID + Doctor ID |
| Medical Record | Record ID | Patient ID + Doctor ID |
| Bill | Bill ID | Patient ID |
| Medicine | Medicine ID | Bills, Prescriptions |

Patient is the root entity — almost everything else points back to a Patient ID. This is why **Patient Management was chosen as the first module to implement**: nothing else can be built meaningfully until a patient can be created and looked up by ID.

---

## 3. Design Decisions for Assessment-I

### 3.1 Why a menu-driven console application
A console menu keeps the focus on program logic rather than interface code. It maps directly onto the course syllabus (loops, conditionals, functions) and is easy to demonstrate in a viva.

### 3.2 Why a list of dictionaries
```python
patients = [
    {"id": "P101", "name": "Rahul Sharma", "age": 24,
     "gender": "Male", "contact": "9876543210"}
]
```
- A **dictionary** groups the fields of one patient under readable keys, so `patient["name"]` is clearer than `patient[1]`.
- A **list** preserves insertion order and allows simple iteration for display and search.
- This structure converts directly into a Pandas DataFrame later (`pd.DataFrame(patients)`), and into a `Patient` class when the project moves to OOP.

### 3.3 Why every function does one thing
`register_patient()` only collects and stores; `display_patient()` only prints; `find_patient_by_id()` only searches. The search function is reused by both the search feature and the duplicate-ID check. When the project grows, each module can be moved into its own file without untangling logic.

### 3.4 Why validation lives in separate helper functions
`get_valid_age()`, `get_valid_gender()`, `get_valid_contact()` and `get_non_empty_input()` each loop until the input is acceptable. This keeps `register_patient()` readable and lets the Doctor module reuse the same validators in Assessment-II without rewriting them.

### 3.5 Why unimplemented modules say so
Options 2–7 print a clear "NOT YET IMPLEMENTED" message. Printing a fake success message would misrepresent the state of the project. The menu still lists all seven modules so the final architecture is visible from the start.

---

## 4. Algorithm — Main Program

```
1. Display welcome message
2. REPEAT
   2.1 Display main menu (options 1-8)
   2.2 Read choice from user
   2.3 IF choice is 1  -> call patient_management()
       ELSE IF choice is 2..7 -> call the corresponding placeholder function
       ELSE IF choice is 8 -> print exit message, BREAK out of the loop
       ELSE -> print "Invalid choice"
3. UNTIL loop is broken
4. END
```

## 5. Algorithm — Register Patient

```
1. REPEAT
   1.1 Read Patient ID
   1.2 IF ID already exists in patients list -> print error, REPEAT
       ELSE BREAK
2. Read Name          (reject if blank)
3. Read Age           (reject if not a digit, or outside 1-120; convert to int)
4. Read Gender        (accept M/F/O only; normalise to Male/Female/Other)
5. Read Contact       (reject unless exactly 10 digits)
6. Build a dictionary from the five fields
7. Append the dictionary to the patients list
8. Print "Patient registered successfully!" and display the record
```

## 6. Algorithm — Search Patient

```
1. IF patients list is empty -> print message, RETURN
2. Read the Patient ID to search for
3. FOR each patient in the patients list
       IF patient's ID matches the search ID (case-insensitive)
           display the record and RETURN
4. Print "No patient found"
```

This is a **linear search**, O(n). It is appropriate for the current record count. If the dataset grows, the list can be replaced with a dictionary keyed by Patient ID for O(1) lookup — a planned improvement.

---

## 7. Known Limitations (current version)

| Limitation | Planned fix |
|------------|-------------|
| Data lost on exit | File handling (CSV/JSON) in Assessment-II |
| Only Patient module works | Doctor, Appointment modules in Assessment-II |
| Function-based, not OOP | Refactor to classes in Assessment-III |
| Linear search | Dictionary keyed by ID if record count grows |
| No exception handling blocks | `try/except` added with file I/O |
| No reporting/analytics | NumPy/Pandas reports in Assessment-IV |
