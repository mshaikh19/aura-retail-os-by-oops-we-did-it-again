from core.kiosk_core_system import KioskCoreSystem
from core.kioskInterface import KioskInterface

import os
import time
import inventory.components.inventoryManager as inventoryManager
from inventory.components.simpleProduct import SimpleProduct

"""
    Color codes for the kiosk interface
"""
class Colors:
    HEADER = '\033[96m'
    BOX = '\033[94m'
    TEXT = '\033[97m'
    SUCCESS = '\033[92m'
    ERROR = '\033[91m'
    WARNING = '\033[93m'
    RESET = '\033[0m'

"""
    Utility Functions
    clearScreen: To clear the terminal screen 
    pauseScreen: To pause the terminal screen until the user presses Enter to continue 
    drawBox: To draw a box around the text to make the interface look like a proper application
"""

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


def pauseScreen():
    input(Colors.TEXT + "\nPress Enter to continue..." + Colors.RESET)


def drawBox(title, content_lines):
    print(Colors.BOX + "+" + "-" * 58 + "+")
    print(f"| {title.center(56)} |")
    print("+" + "-" * 58 + "+")
    
    for line in content_lines:
        print(f"| {line.ljust(56)} |")
    
    print("+" + "-" * 58 + "+" + Colors.RESET)


def selectPaymentMethod():
    clearScreen()
    drawBox(
        "SELECT PAYMENT METHOD",
        [
            "1. UPI",
            "2. Card",
            "3. Wallet"
        ]
    )
    while True:
        choice = input("\nSelect payment option: ")
        if choice == "1":
            return "UPI"
        elif choice == "2":
            return "CARD"
        elif choice == "3":
            return "WALLET"
        else:
            print(Colors.ERROR + "Invalid option. Please choose 1, 2, or 3." + Colors.RESET)


"""
    Screens
    welcomeScreen: Displays the welcome screen to make it look like the system is starting
    mainMenu: Displays the main menu to let the user select an option
    purchaseScreen: Displays the purchase screen to let the user purchase an item
    refundScreen: Displays the refund screen to let the user refund an item
    restockScreen: Displays the restock screen to let the user restock an item
    diagnosticsScreen: Displays the diagnostics screen to let the user run diagnostics
"""

def welcomeScreen():
    clearScreen()
    drawBox(
        "WELCOME",
        [
            "AURA RETAIL OS",
            "",
            "Smart Automated Kiosk System",
            "",
            "Initializing the system..."
        ]
    )
    time.sleep(1.5)


def mainMenu():
    clearScreen()
    drawBox(
        "MAIN MENU",
        [
            "1. Purchase Item",
            "2. Refund Item",
            "3. Restock Inventory",
            "4. Diagnostics",
            "5. Exit"
        ]
    )
    return input("\nSelect an option: ")


def purchaseScreen(interface, products):
    clearScreen()
    drawBox("PURCHASE ITEM", [])

    
    # Alias the method safely so the inventory manager function doesn't crash
    if not hasattr(SimpleProduct, 'get_stock'):
        SimpleProduct.get_stock = SimpleProduct.getStock

    # Create dummy "self" wrapper for the loose function
    class DummySelf:
        def __init__(self, products_dict):
            self.products = products_dict

    print("\n")
    inventoryManager.show_all_products(DummySelf(products))
    print("\n")

    product_name = input("Enter product: ").lower()
    product = products.get(product_name)
    if not product:
        print(Colors.ERROR + "Product not found" + Colors.RESET)
        pauseScreen()

        return

    try:
        qty = int(input("Enter quantity: "))

    except ValueError:
        print(Colors.ERROR + "Invalid quantity" + Colors.RESET)
        pauseScreen()
        return

    print("\n")
    paymentMethod = selectPaymentMethod()

    if not paymentMethod:
        return

    clearScreen()
    drawBox("PROCESSING", ["Please wait..."])
    time.sleep(1)

    interface.purchaseItem(product, qty, paymentMethod)

    print(Colors.SUCCESS + "\nPurchase completed." + Colors.RESET)
    pauseScreen()


def refundScreen(interface):
    clearScreen()
    drawBox("REFUND ITEM", [])

    try:
        amount = float(input("Enter refund amount: "))
    except ValueError:
        print(Colors.ERROR + "Invalid amount" + Colors.RESET)
        pauseScreen()
        return

    print("\n")
    paymentMethod = selectPaymentMethod()

    if not paymentMethod:
        return

    clearScreen()
    drawBox("PROCESSING", ["Processing refund..."])
    time.sleep(1)

    interface.refundTransaction(amount, paymentMethod)

    print(Colors.SUCCESS + "\nRefund completed." + Colors.RESET)
    pauseScreen()


def restockScreen(interface, products):
    clearScreen()
    drawBox("RESTOCK INVENTORY", [])

    product_name = input("Enter product: ").lower()
    product = products.get(product_name)
    if not product:
        print(Colors.ERROR + "Product not found" + Colors.RESET)
        pauseScreen()

        return

    try:
        qty = int(input("Enter quantity: "))
    except ValueError:
        print(Colors.ERROR + "Invalid quantity" + Colors.RESET)
        pauseScreen()
        return

    interface.restockInventory(product, qty)

    print(Colors.SUCCESS + "\nInventory updated." + Colors.RESET)
    pauseScreen()


def diagnosticsScreen(core):
    clearScreen()

    status = core.getSystemStatus()

    drawBox(
        "SYSTEM DIAGNOSTICS",
        [
            f"System Status: {status}",
            "",
            f"Commands Executed: {len(core.getCommandHistory())}"
        ]
    )

    pauseScreen()

def runKiosk():
    from payment.payment_system import PaymentSystem
    from models.productModel import ProductModel
    from inventory.components.simpleProduct import SimpleProduct

    paymentSystem = PaymentSystem()

    catalog_data = {
        "milk": ProductModel("P1", "milk", 50.0, 10),
        "bread": ProductModel("P2", "bread", 30.0, 5),
        "eggs": ProductModel("P3", "eggs", 10.0, 20)
    }

    products = {name: SimpleProduct(model) for name, model in catalog_data.items()}

    core = KioskCoreSystem(inventorySystem=products, paymentSystem=paymentSystem)
    interface = KioskInterface(core)

    welcomeScreen()

    while True:
        choice = mainMenu()

        if choice == "1":
            purchaseScreen(interface, products)

        elif choice == "2":
            refundScreen(interface)

        elif choice == "3":
            restockScreen(interface, products)

        elif choice == "4":
            diagnosticsScreen(core)

        elif choice == "5":
            clearScreen()
            drawBox("SHUTDOWN", ["System shutting down..."])
            break

        else:
            print(Colors.ERROR + "Invalid option" + Colors.RESET)
            time.sleep(1)

>>>>>>> features-maryam
runKiosk()