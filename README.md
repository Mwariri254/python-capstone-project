# Visitor Check-in System

This project is a beginner-friendly Python application for managing visitors entering and leaving a workplace, office, school, or company building. It uses SQLite for storage and pandas for better display of visitor records in a tabular format.

## Project Purpose

Many organizations still use a visitor logbook to record who enters the building, why they are visiting, and when they leave. This system replaces a paper-based register with a simple digital version.

## Features

- Check in a visitor
- Check out a visitor
- Search for a visitor by name, company, phone number, or visitor ID
- View all visitors
- View only today's visitors
- Edit visitor details
- Delete visitor records with confirmation in the web UI
- Store records in SQLite
- Display results using pandas DataFrames

## Database Design

The system uses a single SQLite table called `Visitors`.

### Visitors table

- visitor_id
- name
- company
- phone
- purpose
- check_in_time
- check_out_time
- status

## Python Concepts Used

- Variables
- Input and output
- Functions
- If/elif/else statements
- Loops
- SQLite database operations
- Pandas DataFrames
- CRUD-like operations

## Project Files

- visitor_checkin_system.py - main program logic
- README.md - project documentation
- requirements.txt - project dependencies
- visitor_checkin.db - SQLite database file created when the app runs

## How to Run

### Streamlit UI version

From the project folder, run:

```powershell
cd "C:\Users\Admin\Desktop\python-capstone-project"
.\venv\Scripts\streamlit run app.py
```

This opens the web interface for the visitor check-in system.

### Terminal version

```powershell
cd "C:\Users\Admin\Desktop\python-capstone-project"
.\venv\Scripts\python visitor_checkin_system.py
```

This starts the menu-driven system with options such as:

1. Check in visitor
2. Check out visitor
3. Search visitor
4. View today's visitors
5. View all visitors
6. Edit visitor details
7. Delete visitor
8. Exit

## Database Access

The application creates a local SQLite file named:

```text
visitor_checkin.db
```

This can be opened using DB Browser for SQLite to view records manually.

## Requirements

The project uses Python, the built-in SQLite module, and pandas.

## Future Improvements

Possible upgrades include:

- Add admin login
- Save images or employee ID photos
- Generate daily visitor reports
- Export visitor records to Excel
- Add a nicer graphical interface

## Summary

This project is a practical beginner system that demonstrates how Python can be used to manage visitor logging in a simple and efficient way.