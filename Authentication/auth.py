import json
import os
from getpass import getpass
from Models.user_model import UserModel
from Validation.validators import Validator
from Logs.logger import Logger

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_FILE = os.path.join(BASE_PATH, "Database", "users.json")


class Auth:
    def __init__(self):
        self.admin_email = "admin@highwaydelight.com"
        self.admin_password = "HDAdmin@2024"
        self.admin_name = "Highway Delight Admin"

    def _load_users(self) -> list:
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_users(self, users: list):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4)

    def sign_up(self):
        print("\n--- STAFF SIGN UP ---")
        role = input("  Role (staff only): ").strip().lower()
        if role != "staff":
            print("  ❌ Only staff members can register here.")
            Logger.write_log("Unauthorized sign-up attempt", actor="unknown", details=f"Role attempted: {role}")
            return

        name = input("  Full Name: ").strip()
        email = input("  Email: ").strip()
        mobile = input("  Mobile (10 digits): ").strip()
        experience = input("  Experience (e.g. 2 years): ").strip()
        password = getpass("  Password: ")

        # Validate all fields
        errors = []
        if not Validator.is_valid_name(name):
            errors.append("Name must be at least 2 characters.")
        if not Validator.is_valid_email(email):
            errors.append("Invalid email format.")
        if not Validator.is_valid_mobile(mobile):
            errors.append("Mobile must be exactly 10 digits.")
        if not Validator.is_valid_password(password):
            errors.append("Password must be 8+ chars with uppercase, digit, and special character.")

        if errors:
            print("\n  ❌ Validation failed:")
            for e in errors:
                print(f"     - {e}")
            Logger.write_log("Sign-up validation failed", actor="staff", details=f"Email: {email}")
            return

        users = self._load_users()
        if any(u["email"] == email for u in users):
            print("  ❌ This email is already registered.")
            Logger.write_log("Duplicate sign-up attempt", actor="staff", details=f"Email: {email}")
            return

        user = UserModel(email, name, mobile, experience, "staff", password)
        users.append(user.to_dict())
        self._save_users(users)

        print(f"\n  ✅ Welcome to Highway Delight, {name}! Registration successful.")
        Logger.write_log("Staff registered", actor="staff", details=f"Email: {email}, Name: {name}")

    def sign_in(self):
        print("\n--- SIGN IN ---")
        email = input("  Email: ").strip()
        password = getpass("  Password: ")

        # Check admin
        if email == self.admin_email and password == self.admin_password:
            print(f"\n  ✅ Welcome, {self.admin_name}! (Admin)")
            Logger.write_log("Admin signed in", actor="admin", details=f"Email: {email}")
            return "admin"

        users = self._load_users()
        if not users:
            print("  ❌ No users found. Please sign up first.")
            Logger.write_log("Sign-in failed", actor="unknown", details="User database empty")
            return None

        for u in users:
            if u["email"] == email and u["password"] == password:
                print(f"\n  ✅ Welcome back, {u['name']}! ({u['role'].capitalize()})")
                Logger.write_log("Staff signed in", actor="staff", details=f"Email: {email}, Name: {u['name']}")
                return u["role"]

        print("  ❌ Invalid email or password.")
        Logger.write_log("Sign-in failed", actor="unknown", details=f"Email: {email}")
        return None
