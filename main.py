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
from core.commands.purchase_command import PurchaseCommand
from core.commands.refund_command import RefundCommand
from core.commands.restock_command import RestockCommand

import os

# 🎨 Color Scheme
class Colors:
    HEADER = '\033[96m'
    MENU = '\033[94m'
    SECTION = '\033[93m'
    SUCCESS = '\033[92m'
    ERROR = '\033[91m'
    INPUT = '\033[97m'
    RESET = '\033[0m'


# 🔧 Utilities
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    print(Colors.HEADER + "=" * 70)
    print(" " * 20 + "AURA RETAIL OS")
    print(" " * 12 + "SMART KIOSK MANAGEMENT SYSTEM")
    print("=" * 70 + Colors.RESET)


def print_menu():
    print(Colors.MENU + "\nMAIN MENU")
    print("-" * 70)
    print("1. Purchase Item")
    print("2. Refund Item")
    print("3. Restock Inventory")
    print("4. Run Diagnostics")
    print("5. View Command History")
    print("6. Exit")
    print("-" * 70 + Colors.RESET)


def print_section(title):
    print(Colors.SECTION + "\n" + "-" * 70)
    print(title)
    print("-" * 70 + Colors.RESET)


def get_int(prompt):
    try:
        return int(input(Colors.INPUT + prompt + Colors.RESET))
    except ValueError:
        print(Colors.ERROR + "Invalid number input." + Colors.RESET)
        return None


# 🚀 MAIN SYSTEM
def run_kiosk():

    # Demo inventory
    inventory = {
        "milk": 10,
        "bread": 5,
        "eggs": 20
    }

    core = KioskCoreSystem(inventorySystem=inventory)

    while True:
        clear_screen()
        print_header()
        print_menu()

        choice = input(Colors.INPUT + "\nEnter choice: " + Colors.RESET).strip()

        # 🛒 PURCHASE
        if choice == "1":
            print_section("PURCHASE ITEM")
            product = input("Enter product name: ")
            qty = get_int("Enter quantity: ")

            if qty:
                command = PurchaseCommand(product, qty)
                core.executeCommand(command)

        # 💸 REFUND
        elif choice == "2":
            print_section("REFUND ITEM")
            product = input("Enter product name: ")
            qty = get_int("Enter quantity: ")

            if qty:
                command = RefundCommand(product, qty)
                core.executeCommand(command)

        # 📦 RESTOCK
        elif choice == "3":
            print_section("RESTOCK INVENTORY")
            product = input("Enter product name: ")
            qty = get_int("Enter quantity: ")

            if qty:
                command = RestockCommand(product, qty)
                core.executeCommand(command)

        # ⚙️ DIAGNOSTICS
        elif choice == "4":
            print_section("SYSTEM DIAGNOSTICS")
            print(f"System Status: {core.getSystemStatus()}")

        # 📜 HISTORY
        elif choice == "5":
            print_section("COMMAND HISTORY")

            history = core.getCommandHistory()

            if not history:
                print("No commands executed yet.")
            else:
                for i, cmd in enumerate(history, 1):
                    print(f"{i}. {cmd.__class__.__name__}")

        # 🚪 EXIT
        elif choice == "6":
            print(Colors.ERROR + "\nShutting down system..." + Colors.RESET)
            break

        else:
            print(Colors.ERROR + "\nInvalid choice. Try again." + Colors.RESET)

        input(Colors.INPUT + "\nPress Enter to continue..." + Colors.RESET)


if __name__ == "__main__":
    run_kiosk()