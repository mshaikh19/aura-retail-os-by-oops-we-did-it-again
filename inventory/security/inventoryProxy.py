def show_product(self, product_id):
    print(f"[SECURITY LOG] Viewing product: {product_id}")
    self.inventory_manager.show_product(product_id)


def show_all_products(self):
    print("[SECURITY LOG] Viewing all products")
    self.inventory_manager.show_all_products()