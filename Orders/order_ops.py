import json
import os
from datetime import datetime
from Menu.menu_display import MenuDisplay
from Validation.validators import Validator
from Logs.logger import Logger

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORDERS_FILE = os.path.join(BASE_PATH, "Database", "orders.json")


class OrderOps:

    def _load(self) -> list:
        try:
            with open(ORDERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save(self, orders: list):
        with open(ORDERS_FILE, "w", encoding="utf-8") as f:
            json.dump(orders, f, indent=4)

    def place_order(self):
        print("\n--- PLACE ORDER ---")
        table = input("  Table Number (T1-T12): ").strip().upper()

        if not Validator.is_valid_table(table):
            print("   Invalid table. Use T1 to T12.")
            Logger.write_log("Order failed - invalid table", actor="staff", details=f"Table: {table}")
            return

        menu_items = MenuDisplay().load_menu_as_objects()
        available_codes = {item.code for item in menu_items if item.available}

        print("\n   Tip: View menu from main screen or note item codes.")
        codes_input = input("  Enter Item Codes (e.g S001,M002,B001): ").strip()
        codes = [c.strip().upper() for c in codes_input.split(",") if c.strip()]

        if not codes:
            print("   No codes entered.")
            return

        valid_codes = []
        for code in codes:
            if code in available_codes:
                valid_codes.append(code)
            else:
                menu_obj = next((m for m in menu_items if m.code == code), None)
                if menu_obj and not menu_obj.available:
                    print(f"   '{code}' ({menu_obj.name}) is currently unavailable.")
                else:
                    print(f"  '{code}' not found in menu.")
                Logger.write_log("Invalid item in order", actor="staff", details=f"Code: {code}")

        if not valid_codes:
            print("   No valid items. Order not placed.")
            Logger.write_log("Order failed - no valid items", actor="staff", details=f"Table: {table}")
            return

        orders = self._load()
        order_id = f"ORD{len(orders) + 1:04d}"
        order = {
            "order_id": order_id,
            "table": table,
            "items": valid_codes,
            "status": "active",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        orders.append(order)
        self._save(orders)

        print(f"\n  Order placed! ID: {order_id}")
        print(f"  Table: {table} | Items: {', '.join(valid_codes)}")
        Logger.write_log("Order placed", actor="staff", details=f"ID: {order_id}, Table: {table}, Items: {', '.join(valid_codes)}")

    def view_orders(self):
        print("\n--- ACTIVE ORDERS ---")
        orders = self._load()
        active = [o for o in orders if o.get("status") == "active"]

        if not active:
            print("  No active orders.")
            return

        for o in active:
            print(f"\n  Order ID : {o['order_id']}")
            print(f"  Table    : {o['table']}")
            print(f"  Items    : {', '.join(o['items'])}")
            print(f"  Time     : {o['timestamp']}")
            print("  " + "-" * 40)

    def update_or_cancel_order(self):
        print("\n--- UPDATE / CANCEL ORDER ---")
        order_id = input("  Enter Order ID (e.g. ORD0001): ").strip().upper()
        orders = self._load()

        target = next((o for o in orders if o["order_id"] == order_id and o.get("status") == "active"), None)
        if not target:
            print(f"  Active order '{order_id}' not found.")
            return

        print(f"\n  Found: Table {target['table']} | Items: {', '.join(target['items'])}")
        print("  1. Update Items")
        print("  2. Cancel Order")
        choice = input("  Choice: ").strip()

        if choice == "1":
            new_codes_input = input("  New Item Codes (comma-separated): ").strip()
            new_codes = [c.strip().upper() for c in new_codes_input.split(",") if c.strip()]
            if new_codes:
                target["items"] = new_codes
                target["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._save(orders)
                print(f"   Order {order_id} updated.")
                Logger.write_log("Order updated", actor="admin", details=f"ID: {order_id}, New Items: {', '.join(new_codes)}")
            else:
                print("   No new codes entered.")

        elif choice == "2":
            target["status"] = "cancelled"
            self._save(orders)
            print(f"  Order {order_id} cancelled.")
            Logger.write_log("Order cancelled", actor="admin", details=f"ID: {order_id}, Table: {target['table']}")

        else:
            print("  Invalid choice.")
