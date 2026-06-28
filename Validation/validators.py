import re
from datetime import datetime


class Validator:

    @staticmethod
    def is_valid_name(name: str) -> bool:
        return name.replace(" ", "").isalpha() and len(name.strip()) >= 2

    @staticmethod
    def is_valid_email(email: str) -> bool:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        return bool(re.match(pattern, email.strip()))

    @staticmethod
    def is_valid_mobile(mobile: str) -> bool:
        return mobile.strip().isdigit() and len(mobile.strip()) == 10

    @staticmethod
    def is_valid_password(password: str) -> bool:
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        return True

    @staticmethod
    def is_valid_table(table: str) -> bool:
        valid_tables = [f"T{i}" for i in range(1, 13)]  
        return table.strip().upper() in valid_tables

    @staticmethod
    def is_valid_guests(guests: str) -> bool:
        return guests.strip().isdigit() and 1 <= int(guests.strip()) <= 20

    @staticmethod
    def is_valid_price(price: str) -> bool:
        try:
            return float(price) > 0
        except ValueError:
            return False

    @staticmethod
    def is_valid_code(code: str) -> bool:
        return code.isalnum() and len(code) >= 3

    @staticmethod
    def is_valid_date(date_str: str) -> bool:
        try:
            datetime.strptime(date_str.strip(), "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_time(time_str: str) -> bool:
        try:
            datetime.strptime(time_str.strip(), "%H:%M")
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_experience(exp: str) -> bool:
        return exp.strip().isdigit() and int(exp.strip()) >= 0
