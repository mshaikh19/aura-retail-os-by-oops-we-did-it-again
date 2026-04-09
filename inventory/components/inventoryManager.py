def show_product(self, product_id):
    product = self.get_product(product_id)

    if product is None:
        print(f"Product with ID {product_id} not found")
        return

    print("----- Product Details -----")
    print(f"ID: {product.model.product_id}")
    print(f"Name: {product.model.name}")
    print(f"Price: {product.get_price()}")
    print(f"Stock: {product.get_stock()}")
    print("----------------------------")


def show_all_products(self):
    if not self.products:
        print("Inventory is empty")
        return

    print("===== Inventory =====")
    for product in self.products.values():
        print(f"{product.model.product_id} | {product.model.name} | Stock: {product.get_stock()}")
    print("=====================")