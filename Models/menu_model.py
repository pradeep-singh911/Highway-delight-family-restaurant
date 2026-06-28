class MenuItemModel:
    def __init__(self, code: str, name: str, category: str, price: float, available: bool = True):
        self.code = code
        self.name = name
        self.category = category
        self.price = price
        self.available = available

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "available": self.available
        }
