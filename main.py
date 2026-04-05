from core.kiosk_core_system import KioskCoreSystem
from core.kioskInterface import KioskInterface
import os

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


def printHeader():
    print("=" * 60)
    print(" " * 18 + "AURA RETAIL OS")
    print(" " * 10 + "AUTOMATED KIOSK SYSTEM")
    print("=" * 60)


def printMenu():
    print("\nMAIN MENU")
    print("-" * 60)
    print("1. Purchase Item")
    print("2. Refund Item")
    print("3. Restock Inventory")
    print("4. Run Diagnostics")
    print("5. Exit")
    print("-" * 60)


def printSection(title):
    print("\n" + "-" * 60)
    print(f"{title}")
    print("-" * 60)


def getIntegerInput(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None


def runKiosk():
    inventory = {
        "milk": 10,
        "bread": 5,
        "eggs": 20
    }

    core = KioskCoreSystem(inventory_system=inventory)
    interface = KioskInterface(core)

    while True:
        clearScreen()
        printHeader()
        printMenu()

        choice = input("Enter choice: ").strip()

        if choice == "1":
            printSection("PURCHASE ITEM")
            product = input("Enter product name: ").strip()
            qty = getIntegerInput("Enter quantity: ")

            if qty:
                interface.purchaseItem(product, qty)

        elif choice == "2":
            printSection("REFUND ITEM")
            product = input("Enter product name: ").strip()
            qty = getIntegerInput("Enter quantity: ")

            if qty:
                interface.refundTransaction(product, qty)

        elif choice == "3":
            printSection("RESTOCK INVENTORY")
            product = input("Enter product name: ").strip()
            qty = getIntegerInput("Enter quantity: ")

            if qty:
                interface.restockInventory(product, qty)

        elif choice == "4":
            printSection("SYSTEM DIAGNOSTICS")
            interface.runDiagnostics()

        elif choice == "5":
            print("\nShutting down system...")
            break

        else:
            print("\nInvalid selection. Please try again.")

        input("\nPress Enter to continue...")

runKiosk()