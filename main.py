# from core.kiosk_core_system import KioskCoreSystem
# from core.kioskInterface import KioskInterface
# import os

# def clearScreen():
#     os.system('cls' if os.name == 'nt' else 'clear')


# def printHeader():
#     print("=" * 60)
#     print(" " * 18 + "AURA RETAIL OS")
#     print(" " * 10 + "AUTOMATED KIOSK SYSTEM")
#     print("=" * 60)


# def printMenu():
#     print("\nMAIN MENU")
#     print("-" * 60)
#     print("1. Purchase Item")
#     print("2. Refund Item")
#     print("3. Restock Inventory")
#     print("4. Run Diagnostics")
#     print("5. Exit")
#     print("-" * 60)


# def printSection(title):
#     print("\n" + "-" * 60)
#     print(f"{title}")
#     print("-" * 60)


# def getIntegerInput(prompt):
#     try:
#         return int(input(prompt))
#     except ValueError:
#         print("Invalid input. Please enter a number.")
#         return None


# def runKiosk():
#     inventory = {
#         "milk": 10,
#         "bread": 5,
#         "eggs": 20
#     }

#     core = KioskCoreSystem(inventorySystem=inventory)
#     interface = KioskInterface(core)

#     while True:
#         clearScreen()
#         printHeader()
#         printMenu()

#         choice = input("Enter choice: ").strip()

#         if choice == "1":
#             printSection("PURCHASE ITEM")
#             product = input("Enter product name: ").strip()
#             qty = getIntegerInput("Enter quantity: ")

#             if qty:
#                 interface.purchaseItem(product, qty)

#         elif choice == "2":
#             printSection("REFUND ITEM")
#             product = input("Enter product name: ").strip()
#             qty = getIntegerInput("Enter quantity: ")

#             if qty:
#                 interface.refundTransaction(product, qty)

#         elif choice == "3":
#             printSection("RESTOCK INVENTORY")
#             product = input("Enter product name: ").strip()
#             qty = getIntegerInput("Enter quantity: ")

#             if qty:
#                 interface.restockInventory(product, qty)

#         elif choice == "4":
#             printSection("SYSTEM DIAGNOSTICS")
#             interface.runDiagnostics()

#         elif choice == "5":
#             print("\nShutting down system...")
#             break

#         else:
#             print("\nInvalid selection. Please try again.")

#         input("\nPress Enter to continue...")

# runKiosk()

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
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    input(Colors.TEXT + "\nPress Enter to continue..." + Colors.RESET)


def draw_box(title, content_lines):
    print(Colors.BOX + "+" + "-" * 58 + "+")
    print(f"| {title.center(56)} |")
    print("+" + "-" * 58 + "+")
    
    for line in content_lines:
        print(f"| {line.ljust(56)} |")
    
    print("+" + "-" * 58 + "+" + Colors.RESET)


# 🎬 Screens

def welcome_screen():
    clear()
    draw_box(
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


def main_menu():
    clear()
    draw_box(
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


def purchase_screen(interface):
    clear()
    draw_box("PURCHASE ITEM", [])

    product = input("Enter product: ")
    try:
        qty = int(input("Enter quantity: "))
    except ValueError:
        print(Colors.ERROR + "Invalid quantity" + Colors.RESET)
        pause()
        return

    clear()
    draw_box("PROCESSING", ["Please wait..."])
    time.sleep(1)

    interface.purchaseItem(product, qty)

    print(Colors.SUCCESS + "\nPurchase completed." + Colors.RESET)
    pause()


def refund_screen(interface):
    clear()
    draw_box("REFUND ITEM", [])

    product = input("Enter product: ")
    try:
        qty = int(input("Enter quantity: "))
    except ValueError:
        print(Colors.ERROR + "Invalid quantity" + Colors.RESET)
        pause()
        return

    clear()
    draw_box("PROCESSING", ["Processing refund..."])
    time.sleep(1)

    interface.refundTransaction(product, qty)

    print(Colors.SUCCESS + "\nRefund completed." + Colors.RESET)
    pause()


def restock_screen(interface):
    clear()
    draw_box("RESTOCK INVENTORY", [])

    product = input("Enter product: ")
    try:
        qty = int(input("Enter quantity: "))
    except ValueError:
        print(Colors.ERROR + "Invalid quantity" + Colors.RESET)
        pause()
        return

    interface.restockInventory(product, qty)

    print(Colors.SUCCESS + "\nInventory updated." + Colors.RESET)
    pause()


def diagnostics_screen(core):
    clear()

    status = core.getSystemStatus()

    draw_box(
        "SYSTEM DIAGNOSTICS",
        [
            f"System Status: {status}",
            "",
            f"Commands Executed: {len(core.getCommandHistory())}"
        ]
    )

    pause()


# 🚀 MAIN APP
def run_kiosk():
    inventory = {
        "milk": 10,
        "bread": 5,
        "eggs": 20
    }

    core = KioskCoreSystem(inventorySystem=inventory)
    interface = KioskInterface(core)

    welcome_screen()

    while True:
        choice = main_menu()

        if choice == "1":
            purchase_screen(interface)

        elif choice == "2":
            refund_screen(interface)

        elif choice == "3":
            restock_screen(interface)

        elif choice == "4":
            diagnostics_screen(core)

        elif choice == "5":
            clear()
            draw_box("SHUTDOWN", ["System shutting down..."])
            break

        else:
            print(Colors.ERROR + "Invalid option" + Colors.RESET)
            time.sleep(1)

run_kiosk()