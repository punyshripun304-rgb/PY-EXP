# Viva Voce Preparation Notes

Assessment-I gives 2 marks for explaining the project, so this is mostly about being able to justify choices rather than recite code.

---

## 60-second project pitch

> "My project is a Hospital Management System — a console application in Python that will eventually handle patients, doctors, appointments, medical records, billing, pharmacy and reports. For Assessment-I I've built the menu framework and fully implemented the Patient Management module, because Patient ID is the key that every other module links to. A patient can be registered with validated input, listed in a table, and searched by ID. The other six modules are stubbed with an explicit 'not yet implemented' message, since this is an initial version, not a finished system. Data is currently in memory as a list of dictionaries; file handling and OOP come in the next stages."

---

## Likely questions and answers

**Q: Why did you implement Patient Management first?**
Patient ID is the foreign key for appointments, records and bills. None of those modules can be built meaningfully before a patient can be created and retrieved by ID.

**Q: Why a list of dictionaries and not two parallel lists?**
A dictionary keeps one patient's fields together under named keys, so `patient["age"]` is self-documenting. Parallel lists would need matching indices and break easily. The dictionary structure also converts straight into a Pandas DataFrame or a class later.

**Q: Where is type conversion used?**
In `get_valid_age()`. `input()` always returns a string, so `"24"` is converted with `int(raw_age)` after `isdigit()` confirms it is numeric. Without it, comparisons like `age > 120` would fail.

**Q: Why `isdigit()` before `int()` instead of try/except?**
Both work. I used `isdigit()` here because exception handling hasn't been formally introduced at this point in the project; `try/except` is planned for Assessment-II alongside file I/O, where exceptions are unavoidable.

**Q: Where is `break` used and why?**
Three places: to exit the main menu loop on option 8, to exit the patient sub-menu on option 4, and to exit the Patient-ID loop once a unique ID is accepted. In each case the loop is `while True` and `break` is the exit condition.

**Q: What happens if the user types "abc" at the menu?**
The `if/elif` chain falls through to the `else`, which prints "Invalid choice" and loops back to redisplay the menu. The program does not crash and does not exit.

**Q: How do you prevent duplicate patient IDs?**
`register_patient()` calls `find_patient_by_id()` before accepting an ID. If it returns anything other than `None`, the ID is rejected and re-asked.

**Q: What is the time complexity of your search?**
O(n) — linear search through the list. Fine at this scale. If record count grows I'd switch `patients` to a dictionary keyed by Patient ID, giving O(1) lookup.

**Q: Why does `find_patient_by_id()` return `None` instead of printing?**
Separation of concerns. It's a pure lookup, so it's reusable by both the search feature and the duplicate check. The caller decides what to print.

**Q: What does `if __name__ == "__main__":` do?**
It ensures `main()` runs only when the file is executed directly. If this file is later imported as a module by another file, the menu won't start automatically.

**Q: What are the limitations of the current version?**
Data is not persistent — it's lost on exit. Six modules have no logic. No classes yet. No exception handling. These are stage-wise, not oversights: files in Assessment-II, OOP in Assessment-III, Pandas reporting in Assessment-IV.

**Q: How will you add file handling?**
Two functions, `save_patients()` and `load_patients()`. On exit, write the list of dictionaries to `data/patients.csv` using the `csv` module; on startup, read it back. The in-memory structure doesn't change, so the rest of the code stays the same — that's a benefit of having kept storage separate from logic.

**Q: How will OOP change the design?**
`patients` becomes a list of `Patient` objects instead of dictionaries. Fields become attributes, `display_patient()` becomes a `__str__()` method, validation moves into `__init__`. A base `Person` class can hold shared fields for `Patient` and `Doctor`.

---

## Demo sequence to run live

1. Launch: `python hospital_management.py`
2. Type `9` — show invalid-choice handling.
3. Choose `1` → `1`, register **P101 / Rahul Sharma / 24 / M / 9876543210**.
4. Register a second patient, deliberately typing `abc` for age and `12345` for contact to show validation firing.
5. Try to register a third patient reusing ID `P101` — show duplicate rejection.
6. Choose `2` — show the table of all patients.
7. Choose `3`, search `P101` — found. Search `P999` — not found.
8. Back to main menu, choose `5` (Billing) — show the honest placeholder.
9. Choose `8` to exit cleanly.

---

## Things to have open during the presentation

- The GitHub repository page (public, with README rendering)
- `hospital_management.py` in the editor
- A terminal ready in the project folder
- The commit history (`git log --oneline`)
