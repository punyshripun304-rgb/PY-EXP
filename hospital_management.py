"""
Hospital Management System
Python Programming Lab - Experiential Learning Project
Utility Assessment - I (Initial Version)

Current scope:
    - Menu-driven console application
    - Patient Management module (working: register, view, search)
    - Remaining six modules are declared placeholders, to be built in
      later assessments.

Python concepts used in this version:
    variables, type conversion, if/elif/else, while loops, break/continue,
    lists, dictionaries, user-defined functions, string methods.

Data is currently stored in memory (a list of dictionaries) and is lost
when the program exits. File handling and OOP are planned for Assessment-II.
"""

# ---------------------------------------------------------------------------
# GLOBAL DATA STORE
# ---------------------------------------------------------------------------
# Each patient is a dictionary. All patients are kept in this list.
# In Assessment-II this will be replaced by file storage (CSV/JSON) and
# a Patient class.
patients = []

LINE = "=" * 50


# ---------------------------------------------------------------------------
# HELPER / UTILITY FUNCTIONS
# ---------------------------------------------------------------------------
def print_header(title):
    """Print a formatted section heading."""
    print("\n" + LINE)
    print(title.center(50))
    print(LINE)


def get_non_empty_input(prompt):
    """Keep asking until the user types something that is not blank."""
    while True:
        value = input(prompt).strip()
        if value == "":
            print("  [!] This field cannot be left blank. Please try again.")
            continue
        return value


def get_valid_age(prompt):
    """Read an age and convert it to int, rejecting invalid values."""
    while True:
        raw_age = input(prompt).strip()
        # int() raises ValueError for non-numeric text, so we check first.
        if not raw_age.isdigit():
            print("  [!] Age must be a whole number (example: 24).")
            continue
        age = int(raw_age)              # type conversion: str -> int
        if age <= 0 or age > 120:
            print("  [!] Age must be between 1 and 120.")
            continue
        return age


def get_valid_gender(prompt):
    """Accept M / F / O (or the full word) and normalise it."""
    while True:
        gender = input(prompt).strip().upper()
        if gender in ("M", "MALE"):
            return "Male"
        elif gender in ("F", "FEMALE"):
            return "Female"
        elif gender in ("O", "OTHER"):
            return "Other"
        else:
            print("  [!] Please enter M (Male), F (Female) or O (Other).")


def get_valid_contact(prompt):
    """Validate a 10-digit contact number."""
    while True:
        contact = input(prompt).strip()
        if not contact.isdigit():
            print("  [!] Contact number must contain digits only.")
            continue
        if len(contact) != 10:
            print("  [!] Contact number must be exactly 10 digits.")
            continue
        return contact


def find_patient_by_id(patient_id):
    """Return the patient dictionary with this ID, or None if not found."""
    for patient in patients:
        if patient["id"].upper() == patient_id.upper():
            return patient
    return None


def display_patient(patient):
    """Print one patient's details in a readable block."""
    print("  Patient ID      : " + patient["id"])
    print("  Name            : " + patient["name"])
    print("  Age             : " + str(patient["age"]))
    print("  Gender          : " + patient["gender"])
    print("  Contact Number  : " + patient["contact"])


def module_under_development(module_name):
    """
    Honest placeholder for modules not yet implemented.

    This is deliberate: Assessment-I asks for an initial working version,
    not a simulated complete system.
    """
    print_header(module_name.upper())
    print("  You have selected the " + module_name + " module.")
    print("  Status : NOT YET IMPLEMENTED")
    print("  This module is planned for a later stage of the project.")
    print("  Returning to the main menu...")


# ---------------------------------------------------------------------------
# MODULE 1 : PATIENT MANAGEMENT  (implemented)
# ---------------------------------------------------------------------------
def register_patient():
    """Collect patient details, validate them, and store them."""
    print_header("REGISTER NEW PATIENT")

    # Patient ID must be unique
    while True:
        patient_id = get_non_empty_input("  Enter Patient ID      : ")
        if find_patient_by_id(patient_id) is not None:
            print("  [!] Patient ID '" + patient_id + "' already exists. Use a different ID.")
            continue
        break

    name = get_non_empty_input("  Enter Patient Name    : ")
    age = get_valid_age("  Enter Age             : ")
    gender = get_valid_gender("  Enter Gender (M/F/O)  : ")
    contact = get_valid_contact("  Enter Contact Number  : ")

    # Build the record as a dictionary and add it to the list
    patient = {
        "id": patient_id.upper(),
        "name": name.title(),
        "age": age,
        "gender": gender,
        "contact": contact,
    }
    patients.append(patient)

    print("\n  Patient registered successfully!")
    print("  " + "-" * 40)
    display_patient(patient)
    print("  " + "-" * 40)
    print("  Total patients registered: " + str(len(patients)))


def view_all_patients():
    """Display every registered patient as a simple table."""
    print_header("ALL REGISTERED PATIENTS")

    if len(patients) == 0:
        print("  No patients registered yet.")
        print("  Use option 1 in the Patient Management menu to add one.")
        return

    # Table header
    print("  {:<10} {:<20} {:<5} {:<8} {:<12}".format(
        "ID", "NAME", "AGE", "GENDER", "CONTACT"))
    print("  " + "-" * 57)

    for patient in patients:
        print("  {:<10} {:<20} {:<5} {:<8} {:<12}".format(
            patient["id"],
            patient["name"],
            patient["age"],
            patient["gender"],
            patient["contact"]))

    print("  " + "-" * 57)
    print("  Total records: " + str(len(patients)))


def search_patient():
    """Search for a single patient using the Patient ID."""
    print_header("SEARCH PATIENT")

    if len(patients) == 0:
        print("  No patients registered yet. Nothing to search.")
        return

    patient_id = get_non_empty_input("  Enter Patient ID to search : ")
    patient = find_patient_by_id(patient_id)

    if patient is None:
        print("\n  [!] No patient found with ID '" + patient_id.upper() + "'.")
    else:
        print("\n  Patient found:")
        print("  " + "-" * 40)
        display_patient(patient)
        print("  " + "-" * 40)


def patient_management():
    """Sub-menu for the Patient Management module."""
    while True:
        print_header("PATIENT MANAGEMENT")
        print("  1. Register New Patient")
        print("  2. View All Patients")
        print("  3. Search Patient by ID")
        print("  4. Back to Main Menu")
        print("  " + "-" * 46)

        choice = input("  Enter your choice (1-4): ").strip()

        if choice == "1":
            register_patient()
        elif choice == "2":
            view_all_patients()
        elif choice == "3":
            search_patient()
        elif choice == "4":
            print("  Returning to the main menu...")
            break
        else:
            print("  [!] Invalid choice. Please enter a number from 1 to 4.")


# ---------------------------------------------------------------------------
# MODULES 2 - 7 : PLANNED FOR LATER ASSESSMENTS
# ---------------------------------------------------------------------------
def doctor_management():
    module_under_development("Doctor Management")


def appointment_management():
    module_under_development("Appointment Management")


def medical_records():
    module_under_development("Medical Records")


def billing_management():
    module_under_development("Billing")


def pharmacy_management():
    module_under_development("Pharmacy")


def report_generation():
    module_under_development("Reports")


# ---------------------------------------------------------------------------
# MAIN MENU AND PROGRAM CONTROL
# ---------------------------------------------------------------------------
def display_main_menu():
    """Print the main menu options."""
    print("\n" + LINE)
    print("HOSPITAL MANAGEMENT SYSTEM".center(50))
    print(LINE)
    print("1. Patient Management")
    print("2. Doctor Management")
    print("3. Appointment Management")
    print("4. Medical Records")
    print("5. Billing")
    print("6. Pharmacy")
    print("7. Reports")
    print("8. Exit")
    print(LINE)


def main():
    """Entry point: run the menu loop until the user chooses to exit."""
    print("\nWelcome to the Hospital Management System")
    print("Version 0.1  |  Utility Assessment - I (Initial Version)")

    while True:
        display_main_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            patient_management()
        elif choice == "2":
            doctor_management()
        elif choice == "3":
            appointment_management()
        elif choice == "4":
            medical_records()
        elif choice == "5":
            billing_management()
        elif choice == "6":
            pharmacy_management()
        elif choice == "7":
            report_generation()
        elif choice == "8":
            print("\n" + LINE)
            print("Thank you for using the Hospital Management System.")
            print("Exiting the program...")
            print(LINE)
            break
        else:
            print("\n[!] Invalid choice. Please enter a number between 1 and 8.")


# Standard Python entry-point guard: main() runs only when this file is
# executed directly, not when it is imported by another module later.
if __name__ == "__main__":
    main()
