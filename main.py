from core.kiosk_core_system import KioskCoreSystem
from core.kioskInterface import KioskInterface

from payment.payment_system import PaymentSystem

import os
import time


# 🎨 Colors
class Colors:
    HEADER = '\033[96m'
    BOX = '\033[94m'
    TEXT = '\033[97m'
    SUCCESS = '\033[92m'
    ERROR = '\033[91m'
    WARNING = '\033[93m'
    RESET = '\033[0m'


# 🔧 Utils
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    input("\nPress Enter to continue...")


def draw_box(title, lines):
    print(Colors.BOX + "+" + "-" * 60 + "+")
    print(f"| {title.center(58)} |")
    print("+" + "-" * 60 + "+")
    for line in lines:
        print(f"| {line.ljust(58)} |")
    print("+" + "-" * 60 + "+" + Colors.RESET)


def select_payment_method():
    clear()
    draw_box("SELECT PAYMENT METHOD", [
        "1. UPI",
        "2. Card",
        "3. Wallet"
    ])

    choice = input("Choose option: ")

    if choice == "1":
        return "UPI"
    elif choice == "2":
        return "CARD"
    elif choice == "3":
        return "WALLET"
    else:
        print("Invalid payment method")
        return None


# 🛒 Purchase Screen (with payment)
def purchase_screen(core, inventory):
    from core.commands.purchase_command import PurchaseCommand

    clear()
    draw_box("PURCHASE ITEM", [])

    product_name = input("Enter product name: ").strip().lower()

    product = inventory.get_product(product_name)

    if not product:
        print(Colors.ERROR + f"Product '{product_name}' not found in inventory." + Colors.RESET)
        pause()
        return

    try:
        qty = int(input("Enter quantity: "))
    except:
        print("Invalid quantity")
        pause()
        return

    payment_method = select_payment_method()

    if not payment_method:
        pause()
        return

    core.paymentSystem = PaymentSystem()

    clear()
    draw_box("PROCESSING PAYMENT", ["Please wait..."])
    time.sleep(1)

    command = PurchaseCommand(product, qty, payment_method)
    core.executeCommand(command)

    print(Colors.SUCCESS + "\nTransaction completed." + Colors.RESET)
    pause()


# 💸 Refund Screen
def refund_screen(core):
    from core.commands.refund_command import RefundCommand

    clear()
    draw_box("REFUND", [])

    try:
        amount = float(input("Enter refund amount (Rs.): "))
    except:
        print("Invalid amount")
        pause()
        return

    payment_method = select_payment_method()

    if not payment_method:
        pause()
        return

    core.paymentSystem = PaymentSystem()

    command = RefundCommand(amount, payment_method)
    core.executeCommand(command)

    print(Colors.SUCCESS + "\nRefund processed." + Colors.RESET)
    pause()


# 📦 Restock Screen
def restock_screen(core, inventory):
    from core.commands.restock_command import RestockCommand

    clear()
    draw_box("RESTOCK", [])

    product_name = input("Enter product name: ").strip().lower()

    product = inventory.get_product(product_name)

    if not product:
        print(Colors.ERROR + f"Product '{product_name}' not found in inventory." + Colors.RESET)
        pause()
        return

    try:
        qty = int(input("Enter quantity: "))
    except:
        print("Invalid quantity")
        pause()
        return

    command = RestockCommand(product, qty)
    core.executeCommand(command)

    print(Colors.SUCCESS + "\nInventory updated." + Colors.RESET)
    pause()

# 📋 Inventory Screen
def inventory_screen(inventory):
    clear()
    draw_box("INVENTORY", [])
    inventory.show_all_products()
    pause()


# ⚙️ Diagnostics
def diagnostics_screen(core):
    clear()

    draw_box("SYSTEM STATUS", [
        f"Status: {core.getSystemStatus()}",
        f"Commands Executed: {len(core.getCommandHistory())}"
    ])

    pause()


# 🚀 MAIN
def runKiosk():
    from inventory.components.simpleProduct import SimpleProduct
    from models.productModel import ProductModel
    import inventory.components.inventoryManager as inv_mgr

    # Monkey-patch SimpleProduct to map getPrice -> get_price and getStock -> get_stock
    # since the original inventoryManager.py tries to use the get_price and get_stock variants.
    SimpleProduct.get_price = SimpleProduct.getPrice
    SimpleProduct.get_stock = SimpleProduct.getStock

    # Construct the InventoryManager class inside main.py
    class InventoryManager:
        def __init__(self, products):
            self.products = products

        def get_product(self, product_id):
            return self.products.get(product_id)

        # Bind the functions from the module as methods
        show_product = inv_mgr.show_product
        show_all_products = inv_mgr.show_all_products

    # Pre-seeded inventory with proper SimpleProduct objects
    inventory_products = {
        "milk":  SimpleProduct(ProductModel("P001", "milk",  1.50, stock=10)),
        "bread": SimpleProduct(ProductModel("P002", "bread", 2.00, stock=5)),
        "eggs":  SimpleProduct(ProductModel("P003", "eggs",  3.00, stock=20)),
    }

    # Integrate the dynamic InventoryManager class
    inventory = InventoryManager(inventory_products)

    core = KioskCoreSystem(inventorySystem=inventory)

    while True:
        clear()

        draw_box("AURA RETAIL OS", [
            "1. Purchase",
            "2. Refund",
            "3. Restock",
            "4. View Inventory",
            "5. Diagnostics",
            "6. Exit"
        ])

        choice = input("\nSelect option: ")

        if choice == "1":
            purchase_screen(core, inventory)

        elif choice == "2":
            refund_screen(core)

        elif choice == "3":
            restock_screen(core, inventory)

        elif choice == "4":
            inventory_screen(inventory)

        elif choice == "5":
            diagnostics_screen(core)

        elif choice == "6":
            clear()
            draw_box("EXIT", ["Shutting down system..."])
            break

        else:
            print("Invalid choice")
            time.sleep(1)


runKiosk()