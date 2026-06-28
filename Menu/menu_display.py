import json
import os
from Models.menu_model import MenuItemModel
from Logs.logger import Logger

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MENU_FILE = os.path.join(BASE_PATH, "Database", "menu.json")

DEFAULT_MENU = [
    {"code": "S001", "name": "Pyaaz Ki Kachori",         "category": "Starter",     "price": 80,  "available": True},
    {"code": "S002", "name": "Dal Baati (2 pcs)",         "category": "Starter",     "price": 120, "available": True},
    {"code": "S003", "name": "Mirchi Vada",               "category": "Starter",     "price": 60,  "available": True},
    {"code": "S004", "name": "Mawa Kachori",              "category": "Starter",     "price": 90,  "available": True},
    {"code": "S005", "name": "Paneer Tikka",              "category": "Starter",     "price": 180, "available": True},
    {"code": "S006", "name": "Hara Bhara Kabab (6 pcs)", "category": "Starter",     "price": 150, "available": True},
    {"code": "S007", "name": "Veg Seekh Kabab (6 pcs)",  "category": "Starter",     "price": 160, "available": True},
    {"code": "S008", "name": "Aloo Tikki Chaat",         "category": "Starter",     "price": 80,  "available": True},

    {"code": "M001", "name": "Dal Baati Churma (Thali)", "category": "Main Course", "price": 280, "available": True},
    {"code": "M002", "name": "Gatte Ki Sabzi",           "category": "Main Course", "price": 160, "available": True},
    {"code": "M003", "name": "Gulab jamin ki sabzi",     "category": "Main Course", "price": 200, "available": True},
    {"code": "M004", "name": "Ker Sangri",               "category": "Main Course", "price": 180, "available": True},
    {"code": "M005", "name": "Panchmel Dal",             "category": "Main Course", "price": 150, "available": True},
    {"code": "M006", "name": "Malai kofta",              "category": "Main Course", "price": 160, "available": True},
    {"code": "M007", "name": "Paneer Laal Mirch",        "category": "Main Course", "price": 240, "available": True},
    {"code": "M008", "name": "Rajasthani Kadhi",         "category": "Main Course", "price": 140, "available": True},
    {"code": "M009", "name": "Aloo Mangodi",             "category": "Main Course", "price": 150, "available": True},
    {"code": "M010", "name": "Papad Ki Sabzi",           "category": "Main Course", "price": 130, "available": True},
    {"code": "M011", "name": "Mix Veg Masala",           "category": "Main Course", "price": 160, "available": True},
    {"code": "M012", "name": "Shahi Paneer",             "category": "Main Course", "price": 240, "available": True},
    {"code": "M013", "name": "Kaju dakh (Special)",      "category": "Main Course", "price": 300, "available": True},
    {"code": "M014", "name": "Lasan chutney",            "category": "Main Course", "price": 240, "available": True},


    {"code": "TH01", "name": "Highway Delight Thali",    "category": "Thali",       "price": 320, "available": True},
    {"code": "TH02", "name": "Rajasthani Royal Thali",   "category": "Thali",       "price": 380, "available": True},
    {"code": "TH03", "name": "Mini Thali",               "category": "Thali",       "price": 200, "available": True},

    {"code": "B001", "name": "Bajra Roti",               "category": "Bread",       "price": 20,  "available": True},
    {"code": "B002", "name": "Makki Ki Roti",            "category": "Bread",       "price": 25,  "available": True},
    {"code": "B003", "name": "Tandoori Roti",            "category": "Bread",       "price": 25,  "available": True},
    {"code": "B004", "name": "Butter Naan",              "category": "Bread",       "price": 40,  "available": True},
    {"code": "B005", "name": "Laccha Paratha",           "category": "Bread",       "price": 50,  "available": True},
    {"code": "B006", "name": "Missi Roti",               "category": "Bread",       "price": 30,  "available": True},
    {"code": "B007", "name": "Garlic Naan",              "category": "Bread",       "price": 50,  "available": True},

    
    {"code": "R001", "name": "Steamed Rice",             "category": "Rice",        "price": 80,  "available": True},
    {"code": "R002", "name": "Veg Biryani",              "category": "Rice",        "price": 180, "available": True},
    {"code": "R003", "name": "Rajasthani Pulao",         "category": "Rice",        "price": 160, "available": True},
    {"code": "R004", "name": "Jeera Rice",               "category": "Rice",        "price": 100, "available": True},

   
    {"code": "D001", "name": "Churma Ladoo (2 pcs)",     "category": "Dessert",     "price": 80,  "available": True},
    {"code": "D002", "name": "Malpua with Rabdi",        "category": "Dessert",     "price": 120, "available": True},
    {"code": "D003", "name": "Ghevar",                   "category": "Dessert",     "price": 100, "available": True},
    {"code": "D004", "name": "Gulab Jamun (2 pcs)",      "category": "Dessert",     "price": 80,  "available": True},
    {"code": "D005", "name": "Moong Dal Halwa",          "category": "Dessert",     "price": 110, "available": True},
    {"code": "D006", "name": "Rabdi",                    "category": "Dessert",     "price": 90,  "available": True},
    {"code": "D007", "name": "Balushahi (2 pcs)",        "category": "Dessert",     "price": 70,  "available": True},
    {"code": "D008", "name": "Fruit Cream",              "category": "Dessert",     "price": 80,  "available": True},

    
    {"code": "DR01", "name": "Masala Chaas (Buttermilk)","category": "Drinks",      "price": 50,  "available": True},
    {"code": "DR02", "name": "Aam Panna",                "category": "Drinks",      "price": 60,  "available": True},
    {"code": "DR03", "name": "Rose Sharbat",             "category": "Drinks",      "price": 60,  "available": True},
    {"code": "DR04", "name": "Thandai",                  "category": "Drinks",      "price": 80,  "available": True},
    {"code": "DR05", "name": " Makhaniya Lassi (Sweet)", "category": "Drinks",      "price": 85,  "available": True},
    {"code": "DR06", "name": "Lassi (Salted)",           "category": "Drinks",      "price": 70,  "available": True},
    {"code": "DR07", "name": "Fresh Lime Soda",          "category": "Drinks",      "price": 60,  "available": True},
    {"code": "DR08", "name": "Masala Chai",              "category": "Drinks",      "price": 30,  "available": True},
    {"code": "DR09", "name": "Mineral Water (1L)",       "category": "Drinks",      "price": 30,  "available": True},
]


class MenuDisplay:
    def _load_raw(self) -> list:
        try:
            with open(MENU_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(MENU_FILE, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_MENU, f, indent=4)
            return DEFAULT_MENU

    def show_menu(self):
        items = self._load_raw()
        print("\n" + "=" * 60)
        print("       HIGHWAY DELIGHT — FULL MENU   ")
        print("=" * 60)

        categories = {}
        for item in items:
            categories.setdefault(item.get("category", "Other"), []).append(item)

        for cat, cat_items in categories.items():
            print(f"\n  ── {cat.upper()} ──")
            for item in cat_items:
                status = "✅" if item.get("available", True) else "❌"
                print(f"  {status}  [{item['code']}]  {item['name']:<30} ₹{item['price']}")
        print("\n" + "=" * 60)

    def load_menu_as_objects(self) -> list:
        raw = self._load_raw()
        return [MenuItemModel(i["code"], i["name"], i["category"], i["price"], i.get("available", True))
                for i in raw]


class MenuManager:
    def _load(self) -> list:
        try:
            with open(MENU_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def _save(self, menu: list):
        with open(MENU_FILE, "w", encoding="utf-8") as f:
            json.dump(menu, f, indent=4)

    def manage(self):
        while True:
            print("\n--- MENU MANAGEMENT ---")
            print("  1. View Menu")
            print("  2. Add New Item")
            print("  3. Update Existing Item")
            print("  4. Toggle Item Availability")
            print("  5. Back")
            choice = input("  Choice: ").strip()

            if choice == "1":
                MenuDisplay().show_menu()
            elif choice == "2":
                self._add_item()
            elif choice == "3":
                self._update_item()
            elif choice == "4":
                self._toggle_availability()
            elif choice == "5":
                break
            else:
                print("   Invalid choice.")

    def _add_item(self):
        from Validation.validators import Validator
        print("\n  -- Add Menu Item --")
        code     = input("  Item Code (e.g. S005): ").strip().upper()
        name     = input("  Item Name: ").strip()
        category = input("  Category (Starter/Main Course/Bread/Rice/Dessert/Drinks): ").strip()
        price    = input("  Price (₹): ").strip()

        if not Validator.is_valid_code(code):
            print("   Invalid code. Must be alphanumeric, min 3 chars.")
            return
        if not Validator.is_valid_name(name):
            print("   Invalid name.")
            return
        if not Validator.is_valid_price(price):
            print("   Invalid price.")
            return

        menu = self._load()
        if any(m["code"] == code for m in menu):
            print("  Item code already exists.")
            return

        menu.append({"code": code, "name": name, "category": category,
                     "price": float(price), "available": True})
        self._save(menu)
        print(f"   '{name}' added to menu.")
        Logger.write_log("Menu item added", actor="admin", details=f"{code} | {name} | ₹{price} | {category}")

    def _update_item(self):
        from Validation.validators import Validator
        print("\n  -- Update Menu Item --")
        code = input("  Enter Item Code to update: ").strip().upper()
        menu = self._load()
        item = next((m for m in menu if m["code"] == code), None)

        if not item:
            print("   Item not found.")
            return

        print(f"\n  Current → [{item['code']}] {item['name']} | ₹{item['price']} | {item['category']}")
        print("  (Press Enter to keep current value)")

        new_name     = input(f"  New Name [{item['name']}]: ").strip()
        new_price    = input(f"  New Price [₹{item['price']}]: ").strip()
        new_category = input(f"  New Category [{item['category']}]: ").strip()

        if new_name:
            if not Validator.is_valid_name(new_name):
                print("   Invalid name.")
                return
            item["name"] = new_name
        if new_price:
            if not Validator.is_valid_price(new_price):
                print("   Invalid price.")
                return
            item["price"] = float(new_price)
        if new_category:
            item["category"] = new_category

        self._save(menu)
        print(f"   Item '{code}' updated.")
        Logger.write_log("Menu item updated", actor="admin",
                         details=f"{code} | {item['name']} | ₹{item['price']} | {item['category']}")

    def _toggle_availability(self):
        code = input("  Enter Item Code to toggle: ").strip().upper()
        menu = self._load()
        for item in menu:
            if item["code"] == code:
                item["available"] = not item.get("available", True)
                status = "Available " if item["available"] else "Unavailable "
                self._save(menu)
                print(f"  '{item['name']}' is now {status}")
                Logger.write_log("Menu availability toggled", actor="admin",
                                 details=f"{code} | {item['name']} | {status}")
                return
        print("   Item not found.")
