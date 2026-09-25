# Visitor Check-in System

## Slide 1: Project Overview

- A digital visitor register for offices, schools, and workplaces
- Built with Python and Streamlit
- Stores visitor records in a local SQLite database

**Opening:** This project replaces a paper visitor log with a simple, searchable digital system.

## Slide 2: The Problem

- Paper registers are slow to search
- Visitor details can be difficult to update
- It is easy to lose track of who is still inside
- Old or incorrect records are difficult to manage

## Slide 3: The Solution

The system lets staff:

- Check visitors in with their name, company, phone, and visit purpose
- Check visitors out when they leave
- Search records by name, company, phone, or visitor ID
- See today's arrivals and current visitors

## Slide 4: Main Features

- Dashboard showing arrivals, current visitors, and total records
- Edit visitor details when information changes
- Delete incorrect records with confirmation
- Terminal version for a simple command-line workflow
- Streamlit web interface for everyday use

## Slide 5: Technology and Database

- **Python:** application logic and user actions
- **Streamlit:** interactive web interface
- **SQLite:** local database storage
- **Pandas:** table display and record handling

Each visitor record stores:

`visitor_id`, `name`, `company`, `phone`, `purpose`, `check_in_time`, `check_out_time`, and `status`

## Slide 6: Demonstration

1. Check in a visitor
2. Show the visitor in the register
3. Search by name or visitor ID
4. Check the visitor out
5. Edit a visitor record
6. Delete an incorrect record using confirmation

## Slide 7: Benefits and Future Improvements

**Benefits**

- Faster visitor registration
- Easier record searching
- Clear check-in and check-out status
- Better control over incorrect information

**Future improvements**

- Admin login and permissions
- Visitor photo or ID upload
- Export reports to Excel
- Daily and monthly visitor analytics

## Closing

The Visitor Check-in System demonstrates how Python can solve a practical workplace problem with a simple and usable application.
