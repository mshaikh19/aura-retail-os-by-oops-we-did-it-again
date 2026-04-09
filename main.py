from core.kiosk_core_system import KioskCoreSystem
from core.kioskInterface import KioskInterface
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


# 🔧 Utility Functions
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


# 🎬 Screens

def welcomeScreen():
    clearScreen()
    drawBox(
        "WELCOME",
        [
            "AURA RETAIL OS",
            "",
            "Smart Automated Kiosk System",
            "",
            "Initializing system..."
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
    return input("\nSelect option: ")


def purchaseScreen(interface, products):
    clearScreen()
    drawBox("PURCHASE ITEM", [])

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

    paymentMethod = input("Enter payment method (UPI/CARD/WALLET): ").strip().upper()

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

    paymentMethod = input("Enter payment method (UPI/CARD/WALLET): ").strip().upper()

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


# 🚀 MAIN APP
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

runKiosk()