class UserModel:
    def __init__(self, email: str, name: str, mobile: str, experience: str, role: str, password: str):
        self.email = email
        self.name = name
        self.mobile = mobile
        self.experience = experience
        self.role = role
        self.password = password

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "name": self.name,
            "mobile": self.mobile,
            "experience": self.experience,
            "role": self.role,
            "password": self.password
        }
