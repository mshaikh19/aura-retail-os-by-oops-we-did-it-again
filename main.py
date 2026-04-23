from core.kioskCoreSystem import KioskCoreSystem
from core.kioskInterface import KioskInterface
from payment.paymentSystem import PaymentSystem
from models.productModel import ProductModel
from inventory.components.simpleProduct import SimpleProduct


import os
import time


class Colors:
    HEADER = '\033[96m'    # Cyan
    BLUE = '\033[94m'      # Borders
    SUCCESS = '\033[92m'   # Green
    ERROR = '\033[91m'     # Red
    WARNING = '\033[93m'   # Yellow
    TEXT = '\033[97m'      # White
    RESET = '\033[0m'
    BOLD = '\033[1m'


def clearScreen():
    """ Clears the console window to keep the UI clean """
    os.system('cls' if os.name == 'nt' else 'clear')

def pauseScreen():
    """ Keeps the message on screen until the user is ready """
    print(Colors.TEXT + "\n Press Enter to continue..." + Colors.RESET)
    input()

def showProgress(message, duration=1.2):
    """ List of characters that create the 'spinning' effect """
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    end_time = time.time() + duration
    idx = 0
    while time.time() < end_time:

        """ Move to the beginning of the line each time """
        print(f"\r {Colors.HEADER}{spinner[idx % len(spinner)]} {message}...", end="", flush=True)
        time.sleep(0.08)
        idx += 1
    
    """ Success message after check """
    print(f"\r {Colors.SUCCESS}✓ {message} Done!{Colors.RESET}")

def drawBox(title, lines):    
    width = 60

    # Top border
    print(Colors.BLUE + "╔" + "═"*(width-2) + "╗")
    
    # Title row
    print("║ " + Colors.HEADER + Colors.BOLD + title.center(width-4) + Colors.RESET + Colors.BLUE + " ║")
    
    # Middle separator
    print("╠" + "═"*(width-2) + "╣")
    
    # Content rows
    for line in lines:
        print("║ " + Colors.TEXT + line.ljust(width-4) + Colors.RESET + Colors.BLUE + " ║")
    
    # Bottom border
    print("╚" + "═"*(width-2) + "╝" + Colors.RESET)

""" Display the inventory from products """
def displayInventory(products):

    print(Colors.BLUE + " ┌──────────────────┬────────────┬──────────────┐")
    print(f" │ {Colors.HEADER}PRODUCT{Colors.RESET}{Colors.BLUE:10}     │ {Colors.HEADER}PRICE{Colors.RESET}{Colors.BLUE:7}    │ {Colors.HEADER}STOCK{Colors.RESET}{Colors.BLUE:9}    │")
    print(" ├──────────────────┼────────────┼──────────────┤")
    
    for name, prod in products.items():
        price = f"Rs.{prod.getPrice():.2f}"
        stock = f"{prod.getStock()} units"
        print(Colors.BLUE + f" │ {Colors.TEXT}{name.title():<16} {Colors.BLUE}│ {Colors.TEXT}{price:<10} {Colors.BLUE}│ {Colors.TEXT}{stock:<12} {Colors.BLUE}│")
    
    print(" └──────────────────┴────────────┴──────────────┘" + Colors.RESET)

""" Show the user welcome screen """
def welcomeScreen():
    clearScreen()
    drawBox("AURA RETAIL OS", [
        "Starting System Boot...",
        "Please wait while components initialize."
    ])
    print()
    showProgress("Checking System Modules")
    showProgress("Syncing Inventory DB")
    showProgress("Opening Secure Gateway")
    
    time.sleep(0.5)
    print(Colors.SUCCESS + "\n [BOOT SUCCESS] System is ready for use!" + Colors.RESET)
    time.sleep(1)

def paymentChoice():
    """ Gets payment choice using an easy-to-understand menu """

    clearScreen()
    drawBox("PAYMENT GATEWAY", [
        "1. UPI (Online QR)",
        "2. Credit/Debit Card",
        "3. Digital Wallet"
    ])
    
    while True:
        choice = input("\n Select Payment Method (1-3): ")
        if choice == "1": return "UPI"
        if choice == "2": return "CARD"
        if choice == "3": return "WALLET"
        print(Colors.ERROR + " Invalid selection. Please choose 1, 2, or 3." + Colors.RESET)

def purchaseFlow(interface, products):
    clearScreen()
    print(Colors.BOLD + " --- CURRENT STOCK --- " + Colors.RESET)
    displayInventory(products)

    # Required for project compatibility
    if not hasattr(SimpleProduct, 'get_stock'):
        SimpleProduct.get_stock = SimpleProduct.getStock

    name = input("\n Select Item: ").lower().strip()
    item = products.get(name)
    
    if not item:
        print(Colors.ERROR + " Item not found in catalog." + Colors.RESET)
        pauseScreen()

        return

    try:
        qty = int(input(" Enter quantity: "))
    except ValueError:
        print(Colors.ERROR + " Please enter a valid number." + Colors.RESET)
        pauseScreen()
        return

    if qty > item.getStock():
        print(Colors.ERROR + " Error: Not enough items in stock." + Colors.RESET)
        pauseScreen()
        return

    method = paymentChoice()
    clearScreen()
    showProgress(f"Authorizing {method} Payment")
    
    interface.purchaseItem(item, qty, method)
    print(Colors.SUCCESS + "\n [DONE] Transaction completed successfully!" + Colors.RESET)
    pauseScreen()

def refundFlow(interface):
    clearScreen()
    try:
        amount = float(input(" Enter amount to refund: Rs."))
    except ValueError:
        print(Colors.ERROR + " Please enter a valid number." + Colors.RESET)
        pauseScreen()
        return

    method = paymentChoice()
    showProgress("Contacting Bank for Refund")
    interface.refundTransaction(amount, method)
    print(Colors.SUCCESS + " [DONE] Amount has been reversed." + Colors.RESET)
    pauseScreen()

def restockFlow(interface, products):
    clearScreen()
    name = input(" Product to Restock: ").lower().strip()
    item = products.get(name)
    
    if not item:
        print(Colors.ERROR + " Product not found." + Colors.RESET)
        pauseScreen()

        return

    try:
        qty = int(input(" Quantity to add: "))
    except ValueError:
        print(Colors.ERROR + " Please enter a number." + Colors.RESET)
        pauseScreen()
        return

    interface.restockInventory(item, qty)
    print(Colors.SUCCESS + f" [DONE] Inventory updated." + Colors.RESET)
    pauseScreen()

def diagnosticsFlow(core):
    clearScreen()
    status = core.getSystemStatus()
    drawBox("KIOSK DIAGNOSTICS", [
        f"Health Status: {status}",
        f"Total Commands: {len(core.getCommandHistory())}",
        "Security Check: All Passed"
    ])
    pauseScreen()

def runKiosk():

    # Setup core systems
    payment_sys = PaymentSystem()
    catalog = {
        "milk":  ProductModel("P1", "milk", 50.0, 10),
        "bread": ProductModel("P2", "bread", 30.0, 5),
        "eggs":  ProductModel("P3", "eggs", 10.0, 20)
    }
    products = {name: SimpleProduct(model) for name, model in catalog.items()}

    # Initialize Core & Interface
    core = KioskCoreSystem(inventorySystem=products, paymentSystem=payment_sys)
    interface = KioskInterface(core)

    welcomeScreen()

    while True:
        clearScreen()
        drawBox("MAIN MENU", [
            "1. Purchase Product",
            "2. Process Refund",
            "3. Restock Inventory",
            "4. System Diagnostics",
            "5. Exit System"
        ])
        choice = input("\n Choose Action (1-5): ")

        if choice == "1":
            purchaseFlow(interface, products)
        elif choice == "2":
            refundFlow(interface)
        elif choice == "3":
            restockFlow(interface, products)
        elif choice == "4":
            diagnosticsFlow(core)
        elif choice == "5":
            print(Colors.WARNING + " Powering Down... Goodbye!" + Colors.RESET)
            time.sleep(1)
            break
        else:
            print(Colors.ERROR + " Invalid option." + Colors.RESET)
            time.sleep(1)

runKiosk()