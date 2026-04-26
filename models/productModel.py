class ProductModel:
    def __init__(self, product_id, name, price, stock=0, required_module=None):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock
        
        # 🔥 NEW: hardware dependency
        self.required_module = required_module

    def __repr__(self):
        return f"ProductModel({self.product_id}, {self.name}, Stock={self.stock})"