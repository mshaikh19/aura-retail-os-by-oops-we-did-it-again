from core.kiosk_core import KioskCoreSystem
from core.kiosk_interface import KioskInterface

from payment.payment_system import PaymentSystem
from payment.adapters.upi_adapter import UPIAdapter
from payment.adapters.card_adapter import CardAdapter
from payment.adapters.wallet_adapter import WalletAdapter

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


# 💳 Payment Selection
def select_payment_method():
    clear()
    draw_box("SELECT PAYMENT METHOD", [
        "1. UPI",
        "2. Card",
        "3. Wallet"
    ])

    choice = input("Choose option: ")

    if choice == "1":
        return UPIAdapter()
    elif choice == "2":
        return CardAdapter()
    elif choice == "3":
        return WalletAdapter()
    else:
        print(Colors.ERROR + "Invalid payment method" + Colors.RESET)
        return None


# 🛒 Purchase Screen (with payment)
def purchase_screen(interface, core):
    clear()
    draw_box("PURCHASE ITEM", [])

    product = input("Enter product: ")

    try:
        qty = int(input("Enter quantity: "))
    except:
        print("Invalid quantity")
        pause()
        return

    # 💳 Payment Selection
    payment_processor = select_payment_method()

    if not payment_processor:
        pause()
        return

    # Attach payment system to core
    core.paymentSystem = PaymentSystem(payment_processor)

    clear()
    draw_box("PROCESSING PAYMENT", ["Please wait..."])
    time.sleep(1)

    interface.purchaseItem(product, qty)

    print(Colors.SUCCESS + "\nTransaction completed." + Colors.RESET)
    pause()


# 💸 Refund Screen
def refund_screen(interface):
    clear()
    draw_box("REFUND", [])

    txn = input("Enter transaction ID: ")

    interface.refundTransaction(txn)

    print(Colors.SUCCESS + "\nRefund processed." + Colors.RESET)
    pause()


# 📦 Restock Screen
def restock_screen(interface):
    clear()
    draw_box("RESTOCK", [])

    product = input("Enter product: ")

    try:
        qty = int(input("Enter quantity: "))
    except:
        print("Invalid quantity")
        pause()
        return

    interface.restockInventory(product, qty)

    print(Colors.SUCCESS + "\nInventory updated." + Colors.RESET)
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
    inventory = {
        "milk": 10,
        "bread": 5,
        "eggs": 20
    }

    core = KioskCoreSystem(inventorySystem=inventory)
    interface = KioskInterface(core)

    while True:
        clear()

        draw_box("AURA RETAIL OS", [
            "1. Purchase",
            "2. Refund",
            "3. Restock",
            "4. Diagnostics",
            "5. Exit"
        ])

        choice = input("\nSelect option: ")

        if choice == "1":
            purchase_screen(interface, core)

        elif choice == "2":
            refund_screen(interface)

        elif choice == "3":
            restock_screen(interface)

        elif choice == "4":
            diagnostics_screen(core)

        elif choice == "5":
            clear()
            draw_box("EXIT", ["Shutting down system..."])
            break

        else:
            print("Invalid choice")
            time.sleep(1)


run_kiosk()