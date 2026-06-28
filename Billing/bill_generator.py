import json
import os
from datetime import datetime
from Validation.validators import Validator
from Logs.logger import Logger

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORDERS_FILE = os.path.join(BASE_PATH, "Database", "orders.json")
BOOKINGS_FILE = os.path.join(BASE_PATH, "Database", "bookings.json")
MENU_FILE = os.path.join(BASE_PATH, "Database", "menu.json")
BILLS_FILE = os.path.join(BASE_PATH, "Database", "bills.json")

GST_RATE = 0.05  # 5% GST


class BillGenerator:

    def _load_json(self, path: str) -> list:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def generate_bill(self):
        print("\n--- GENERATE BILL ---")
        table = input("  Enter Table Number (T1–T12): ").strip().upper()

        if not Validator.is_valid_table(table):
            print("  ❌ Invalid table number.")
            return

        orders = self._load_json(ORDERS_FILE)
        order = next((o for o in orders if o.get("table") == table and o.get("status") == "active"), None)

        if not order:
            print(f"  ❌ No active order found for Table {table}.")
            return

        item_codes = order.get("items", [])
        if not item_codes:
            print("  ❌ Order has no items.")
            return

        menu = self._load_json(MENU_FILE)
        if not menu:
            print("  ❌ Menu data missing.")
            return

        # Count quantities
        item_count = {}
        for code in item_codes:
            item_count[code] = item_count.get(code, 0) + 1

        subtotal = 0
        item_details = []
        for code, qty in item_count.items():
            menu_item = next((m for m in menu if m["code"] == code), None)
            if menu_item:
                price = menu_item["price"]
                line_total = price * qty
                subtotal += line_total
                item_details.append({
                    "code": code,
                    "name": menu_item["name"],
                    "quantity": qty,
                    "unit_price": price,
                    "total_price": line_total
                })

        gst = round(subtotal * GST_RATE, 2)
        total = round(subtotal + gst, 2)

        # Get customer info from bookings
        bookings = self._load_json(BOOKINGS_FILE)
        customer = next((b for b in bookings if b.get("table") == table and b.get("status") == "active"), {})
        customer_name = customer.get("name", "Walk-in Customer")
        customer_mobile = customer.get("mobile", "N/A")
        guests = customer.get("guests", 1)

        # Save bill
        bills = self._load_json(BILLS_FILE)
        bill_id = f"BILL{len(bills) + 1:04d}"
        bill = {
            "bill_id": bill_id,
            "order_id": order.get("order_id", "N/A"),
            "table": table,
            "customer_name": customer_name,
            "customer_mobile": customer_mobile,
            "guests": guests,
            "items": item_details,
            "subtotal": subtotal,
            "gst": gst,
            "gst_rate": f"{int(GST_RATE * 100)}%",
            "total": total,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        bills.append(bill)
        with open(BILLS_FILE, "w", encoding="utf-8") as f:
            json.dump(bills, f, indent=4)

        # Mark order as billed
        for o in orders:
            if o.get("table") == table and o.get("status") == "active":
                o["status"] = "billed"
        with open(ORDERS_FILE, "w", encoding="utf-8") as f:
            json.dump(orders, f, indent=4)

        # Mark booking as completed
        for b in bookings:
            if b.get("table") == table and b.get("status") == "active":
                b["status"] = "completed"
        with open(BOOKINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(bookings, f, indent=4)

        # Print bill
        self._print_bill(bill)
        Logger.write_log("Bill generated", actor="staff",
                         details=f"ID: {bill_id}, Table: {table}, Total: ₹{total}, Customer: {customer_name}")

    def _print_bill(self, bill: dict):
        print("\n" + "=" * 55)
        print("       🛣️  HIGHWAY DELIGHT FAMILY RESTAURANT  🛣️")
        print("          NH-48, Near Highway Junction")
        print("          Phone: +91-98765-43210")
        print("=" * 55)
        print(f"  Bill ID   : {bill['bill_id']}")
        print(f"  Table     : {bill['table']}")
        print(f"  Customer  : {bill['customer_name']}")
        print(f"  Mobile    : {bill['customer_mobile']}")
        print(f"  Guests    : {bill['guests']}")
        print(f"  Date/Time : {bill['timestamp']}")
        print("-" * 55)
        print(f"  {'Item':<25} {'Qty':<5} {'Rate':<8} {'Amount'}")
        print("-" * 55)
        for item in bill["items"]:
            print(f"  {item['name']:<25} {item['quantity']:<5} ₹{item['unit_price']:<7} ₹{item['total_price']}")
        print("-" * 55)
        print(f"  {'Subtotal':<40} ₹{bill['subtotal']}")
        print(f"  {'GST (' + bill['gst_rate'] + ')':<40} ₹{bill['gst']}")
        print("=" * 55)
        print(f"  {'TOTAL AMOUNT':<40} ₹{bill['total']}")
        print("=" * 55)
        print("      Thank you for dining at Highway Delight! 🙏")
        print("         Drive Safe & Visit Again Soon!")
        print("=" * 55)

    def view_bills(self):
        print("\n--- BILL HISTORY ---")
        bills = self._load_json(BILLS_FILE)
        if not bills:
            print("  No bills generated yet.")
            return

        print(f"\n  {'Bill ID':<10} {'Table':<6} {'Customer':<20} {'Total':<10} {'Time'}")
        print("  " + "-" * 70)
        for b in bills:
            print(f"  {b['bill_id']:<10} {b['table']:<6} {b['customer_name']:<20} ₹{b['total']:<9} {b['timestamp']}")
