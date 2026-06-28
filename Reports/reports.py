import json
import os
from datetime import datetime, timedelta

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BILLS_FILE    = os.path.join(BASE_PATH, "Database", "bills.json")
ORDERS_FILE   = os.path.join(BASE_PATH, "Database", "orders.json")
BOOKINGS_FILE = os.path.join(BASE_PATH, "Database", "bookings.json")
USERS_FILE    = os.path.join(BASE_PATH, "Database", "users.json")


class Reports:
    def __init__(self):
        self.today      = datetime.now().date()
        self.month_ago  = self.today - timedelta(days=30)

    def _load(self, path: str) -> list:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def _parse_date(self, ts: str):
        try:
            return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").date()
        except:
            return None

    def daily_sales(self):
        print(f"\n--- DAILY SALES ({self.today}) ---")
        bills = self._load(BILLS_FILE)
        total = 0
        found = False
        for b in bills:
            if self._parse_date(b["timestamp"]) == self.today:
                print(f"  {b['bill_id']} | {b['table']} | {b.get('customer_name','Walk-in')} | ₹{b['total']}")
                total += b["total"]
                found = True
        if not found:
            print("  No bills generated today.")
        print(f"\n  Today's Total Revenue : ₹{round(total, 2)}")

    def daily_orders(self):
        print(f"\n--- DAILY ORDERS ({self.today}) ---")
        orders = self._load(ORDERS_FILE)
        count = sum(1 for o in orders if self._parse_date(o["timestamp"]) == self.today)
        print(f"  Total Orders Today    : {count}")

    def daily_bookings(self):
        print(f"\n--- DAILY BOOKINGS ({self.today}) ---")
        bookings = self._load(BOOKINGS_FILE)
        count = sum(1 for b in bookings if self._parse_date(b["timestamp"]) == self.today)
        print(f"  Total Bookings Today  : {count}")

  
    def monthly_sales(self):
        print(f"\n--- MONTHLY SALES (Last 30 Days) ---")
        bills = self._load(BILLS_FILE)
        total = 0
        count = 0
        for b in bills:
            d = self._parse_date(b["timestamp"])
            if d and self.month_ago <= d <= self.today:
                total += b["total"]
                count += 1
        print(f"  Bills Generated       : {count}")
        print(f"  Total Revenue         : ₹{round(total, 2)}")
        if count:
            print(f"  Average Bill          : ₹{round(total / count, 2)}")

    def monthly_orders(self):
        print(f"\n--- MONTHLY ORDERS (Last 30 Days) ---")
        orders = self._load(ORDERS_FILE)
        count = sum(1 for o in orders
                    if (d := self._parse_date(o["timestamp"])) and self.month_ago <= d <= self.today)
        print(f"  Total Orders          : {count}")

    def monthly_bookings(self):
        print(f"\n--- MONTHLY BOOKINGS (Last 30 Days) ---")
        bookings = self._load(BOOKINGS_FILE)
        count = sum(1 for b in bookings
                    if (d := self._parse_date(b["timestamp"])) and self.month_ago <= d <= self.today)
        print(f"  Total Bookings        : {count}")

    def top_selling_items(self):
        print("\n--- TOP SELLING ITEMS (All Time) ---")
        bills = self._load(BILLS_FILE)
        if not bills:
            print("  No billing data.")
            return
        item_sales = {}
        for b in bills:
            for item in b.get("items", []):
                name = item["name"]
                item_sales.setdefault(name, {"qty": 0, "revenue": 0})
                item_sales[name]["qty"]     += item["quantity"]
                item_sales[name]["revenue"] += item["total_price"]

        sorted_items = sorted(item_sales.items(), key=lambda x: x[1]["qty"], reverse=True)
        print(f"\n  {'Item':<30} {'Qty Sold':<12} {'Revenue'}")
        print("  " + "-" * 55)
        for name, data in sorted_items[:10]:
            print(f"  {name:<30} {data['qty']:<12} ₹{data['revenue']}")

    def table_utilization(self):
        print("\n--- TABLE UTILIZATION ---")
        bookings = self._load(BOOKINGS_FILE)
        table_counts = {}
        for b in bookings:
            t = b.get("table", "Unknown")
            table_counts[t] = table_counts.get(t, 0) + 1
        if not table_counts:
            print("  No booking data.")
            return
        for t in sorted(table_counts):
            bar = "█" * table_counts[t]
            print(f"  {t:<5} {bar} ({table_counts[t]})")

    def staff_report(self):
        print("\n--- STAFF LIST ---")
        users = self._load(USERS_FILE)
        if not users:
            print("  No staff registered.")
            return
        print(f"\n  {'Name':<20} {'Email':<30} {'Mobile':<12} {'Experience'}")
        print("  " + "-" * 75)
        for u in users:
            print(f"  {u['name']:<20} {u['email']:<30} {u['mobile']:<12} {u.get('experience','N/A')}")
