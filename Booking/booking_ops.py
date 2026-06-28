import json
import os
from datetime import datetime, time, timedelta
from Validation.validators import Validator
from Logs.logger import Logger

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKINGS_FILE = os.path.join(BASE_PATH, "Database", "bookings.json")

OPEN_TIME  = time(9, 0)   
CLOSE_TIME = time(23, 0)  


class BookingOps:

    def _load(self) -> list:
        try:
            with open(BOOKINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save(self, bookings: list):
        with open(BOOKINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(bookings, f, indent=4)

    def book_table(self):
        print("\n--- TABLE BOOKING ---")
        table = input("  Table Number (T1 - 12): ").strip().upper()
        if not Validator.is_valid_table(table):
            print("   Invalid table. Use T1 to T12.")
            return

        name     = input("  Customer Name: ").strip()
        mobile   = input("  Mobile Number (10 digits): ").strip()
        guests   = input("  Number of Guests (1-20): ").strip()
        date_str = input("  Booking Date (YYYY-MM-DD): ").strip()
        time_str = input("  Booking Time (HH:MM, 24-hr): ").strip()

        if not Validator.is_valid_name(name):
            print("   Invalid name.")
            return
        if not Validator.is_valid_mobile(mobile):
            print("   Mobile must be 10 digits.")
            return
        if not Validator.is_valid_guests(guests):
            print("   Guests must be between 1 and 20.")
            return
        if not Validator.is_valid_date(date_str):
            print("   Invalid date format. Use YYYY-MM-DD.")
            return
        if not Validator.is_valid_time(time_str):
            print("   Invalid time format. Use HH:MM (24-hr).")
            return
        
        booking_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        now = datetime.now()

        
        if booking_dt.date() < now.date():
            print("   Booking date cannot be in the past.")
            return
        if booking_dt.date() == now.date() and booking_dt.time() <= now.time():
            print("   Booking time must be later than current time.")
            return
        if not (OPEN_TIME <= booking_dt.time() <= CLOSE_TIME):
            print(f"   We're open 09:00–23:00 only.")
            return

        bookings = self._load()

        
        conflict = any(
            b["table"] == table and b["date"] == date_str and b["time"] == time_str
            and b.get("status") == "active"
            for b in bookings
        )

        if conflict:
            print(f"   Table {table} is already booked at {time_str} on {date_str}.")
            suggested = booking_dt
            while True:
                suggested += timedelta(minutes=30)
                if suggested.time() > CLOSE_TIME:
                    print("    No more slots available that day.")
                    return
                slot_taken = any(
                    b["table"] == table and
                    b["date"] == suggested.strftime("%Y-%m-%d") and
                    b["time"] == suggested.strftime("%H:%M") and
                    b.get("status") == "active"
                    for b in bookings
                )
                if not slot_taken:
                    print(f"   Next available slot: {suggested.strftime('%Y-%m-%d %H:%M')}")
                    return

        booking_id = f"BK{len(bookings) + 1:03d}"
        booking = {
            "booking_id": booking_id,
            "table": table,
            "name": name,
            "mobile": mobile,
            "guests": int(guests),
            "date": date_str,
            "time": time_str,
            "status": "active",
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S")
        }
        bookings.append(booking)
        self._save(bookings)

        print(f"\n  ✅ Table {table} booked for {name}")
        print(f"  📅 Date: {date_str}  ⏰ Time: {time_str}  👥 Guests: {guests}")
        print(f"  📋 Booking ID: {booking_id}")
        Logger.write_log("Table booked", actor="staff",
                         details=f"ID: {booking_id}, Table: {table}, Date: {date_str}, Time: {time_str}, Customer: {name}")

    def view_bookings(self):
        print("\n--- ACTIVE BOOKINGS ---")
        bookings = self._load()
        active = [b for b in bookings if b.get("status") == "active"]

        if not active:
            print("  No active bookings.")
            return

        print(f"\n  {'ID':<8} {'Table':<6} {'Name':<20} {'Date':<12} {'Time':<8} {'Guests':<8} {'Mobile'}")
        print("  " + "-" * 75)
        for b in active:
            print(f"  {b['booking_id']:<8} {b['table']:<6} {b['name']:<20} "
                  f"{b.get('date','N/A'):<12} {b.get('time','N/A'):<8} {b['guests']:<8} {b['mobile']}")

    def cancel_booking(self):
        print("\n--- CANCEL BOOKING ---")
        booking_id = input("  Enter Booking ID (e.g. BK001): ").strip().upper()
        bookings = self._load()

        for b in bookings:
            if b["booking_id"] == booking_id and b.get("status") == "active":
                b["status"] = "cancelled"
                self._save(bookings)
                print(f"   Booking {booking_id} cancelled.")
                Logger.write_log("Booking cancelled", actor="staff",
                                 details=f"ID: {booking_id}, Table: {b['table']}, Date: {b.get('date')}")
                return

        print(f"  Active booking '{booking_id}' not found.")

    def get_customer_for_table(self, table: str) -> dict:
        bookings = self._load()
        for b in bookings:
            if b["table"] == table and b.get("status") == "active":
                return b
        return {}
