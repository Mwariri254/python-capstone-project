import sqlite3
from datetime import datetime

import pandas as pd

DB_NAME = "visitor_checkin.db"


def initialize_database(db_name: str = DB_NAME) -> None:
    """Create the SQLite database and visitors table if it does not exist."""
    with sqlite3.connect(db_name) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS Visitors (
                visitor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                company TEXT NOT NULL,
                phone TEXT,
                purpose TEXT,
                check_in_time TEXT NOT NULL,
                check_out_time TEXT,
                status TEXT NOT NULL DEFAULT 'Checked In'
            )
            """
        )
        conn.commit()


def check_in_visitor(name: str, company: str, phone: str, purpose: str, db_name: str = DB_NAME) -> int:
    """Register a visitor and record the time they checked in."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(db_name) as conn:
        cursor = conn.execute(
            """
            INSERT INTO Visitors (name, company, phone, purpose, check_in_time, status)
            VALUES (?, ?, ?, ?, ?, 'Checked In')
            """,
            (name, company, phone, purpose, current_time),
        )
        conn.commit()
        return cursor.lastrowid


def view_all_visitors(db_name: str = DB_NAME) -> pd.DataFrame:
    """Return all visitors as a DataFrame."""
    with sqlite3.connect(db_name) as conn:
        return pd.read_sql_query("SELECT * FROM Visitors ORDER BY visitor_id", conn)


def search_visitors(search_term: str, db_name: str = DB_NAME) -> pd.DataFrame:
    """Search visitors by name, company, phone, or visitor ID."""
    term = f"%{search_term.strip()}%"
    with sqlite3.connect(db_name) as conn:
        return pd.read_sql_query(
            """
            SELECT * FROM Visitors
            WHERE name LIKE ? OR company LIKE ? OR phone LIKE ? OR CAST(visitor_id AS TEXT) LIKE ?
            ORDER BY visitor_id
            """,
            conn,
            params=(term, term, term, term),
        )


def view_todays_visitors(db_name: str = DB_NAME) -> pd.DataFrame:
    """Return visitors who checked in today."""
    today = datetime.now().strftime("%Y-%m-%d")
    with sqlite3.connect(db_name) as conn:
        return pd.read_sql_query(
            "SELECT * FROM Visitors WHERE substr(check_in_time, 1, 10) = ? ORDER BY visitor_id",
            conn,
            params=(today,),
        )


def check_out_visitor(visitor_id: int, db_name: str = DB_NAME) -> bool:
    """Mark a visitor as checked out."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(db_name) as conn:
        visitor = conn.execute(
            "SELECT visitor_id FROM Visitors WHERE visitor_id = ?",
            (visitor_id,),
        ).fetchone()

        if not visitor:
            return False

        conn.execute(
            "UPDATE Visitors SET check_out_time = ?, status = 'Checked Out' WHERE visitor_id = ?",
            (current_time, visitor_id),
        )
        conn.commit()
        return True


def edit_visitor(visitor_id: int, name: str = None, company: str = None, phone: str = None, purpose: str = None, db_name: str = DB_NAME) -> bool:
    """Edit the details of an existing visitor."""
    with sqlite3.connect(db_name) as conn:
        visitor = conn.execute(
            "SELECT name, company, phone, purpose FROM Visitors WHERE visitor_id = ?",
            (visitor_id,),
        ).fetchone()

        if not visitor:
            return False

        updated_name = name if name is not None else visitor[0]
        updated_company = company if company is not None else visitor[1]
        updated_phone = phone if phone is not None else visitor[2]
        updated_purpose = purpose if purpose is not None else visitor[3]

        conn.execute(
            """
            UPDATE Visitors
            SET name = ?, company = ?, phone = ?, purpose = ?
            WHERE visitor_id = ?
            """,
            (updated_name, updated_company, updated_phone, updated_purpose, visitor_id),
        )
        conn.commit()
        return True


def delete_visitor(visitor_id: int, db_name: str = DB_NAME) -> bool:
    """Delete an existing visitor record."""
    with sqlite3.connect(db_name) as conn:
        cursor = conn.execute("DELETE FROM Visitors WHERE visitor_id = ?", (visitor_id,))
        conn.commit()
        return cursor.rowcount > 0


def display_menu() -> None:
    print("\n=== Visitor Check-in System ===")
    print("1. Check in visitor")
    print("2. Check out visitor")
    print("3. Search visitor")
    print("4. View today's visitors")
    print("5. View all visitors")
    print("6. Edit visitor details")
    print("7. Delete visitor")
    print("8. Exit")


def main() -> None:
    initialize_database()

    while True:
        display_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Enter visitor name: ").strip()
            company = input("Enter company name: ").strip()
            phone = input("Enter phone number: ").strip()
            purpose = input("Enter purpose of visit: ").strip()
            visitor_id = check_in_visitor(name, company, phone, purpose)
            print(f"Visitor checked in successfully. Visitor ID: {visitor_id}")

        elif choice == "2":
            visitor_id = int(input("Enter visitor ID to check out: ").strip())
            success = check_out_visitor(visitor_id)
            if success:
                print("Visitor checked out successfully.")
            else:
                print("Visitor not found.")

        elif choice == "3":
            search_term = input("Enter visitor name, company, phone or ID: ").strip()
            results = search_visitors(search_term)
            if results.empty:
                print("No matching visitors found.")
            else:
                print(results.to_string(index=False))

        elif choice == "4":
            today_visitors = view_todays_visitors()
            if today_visitors.empty:
                print("No visitors checked in today.")
            else:
                print(today_visitors.to_string(index=False))

        elif choice == "5":
            all_visitors = view_all_visitors()
            if all_visitors.empty:
                print("No visitors found.")
            else:
                print(all_visitors.to_string(index=False))

        elif choice == "6":
            visitor_id = int(input("Enter visitor ID to update: ").strip())
            name = input("Enter new name (leave blank to keep current): ").strip()
            company = input("Enter new company (leave blank to keep current): ").strip()
            phone = input("Enter new phone (leave blank to keep current): ").strip()
            purpose = input("Enter new purpose (leave blank to keep current): ").strip()

            success = edit_visitor(
                visitor_id,
                name=name or None,
                company=company or None,
                phone=phone or None,
                purpose=purpose or None,
            )

            if success:
                print("Visitor details updated successfully.")
            else:
                print("Visitor not found.")

        elif choice == "7":
            visitor_id = int(input("Enter visitor ID to delete: ").strip())
            success = delete_visitor(visitor_id)
            if success:
                print("Visitor deleted successfully.")
            else:
                print("Visitor not found.")

        elif choice == "8":
            print("Thanks for using the Visitor Check-in System.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
