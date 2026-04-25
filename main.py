import sys
import io
# Force UTF-8 encoding for premium UI rendering on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from core.kioskCoreSystem import KioskCoreSystem
from core.kioskInterface import KioskInterface
from payment.paymentSystem import PaymentSystem
from models.productModel import ProductModel
from inventory.components.simpleProduct import SimpleProduct
from inventory.components.productBundle import ProductBundle
from inventory.components.inventoryManager import InventorySystem
from inventory.security.inventoryProxy import SecureInventoryProxy
from registry.central_registry import CentralRegistry


import os
import time


class Colors:
    HEADER = '\033[95m'    # Magenta/Purple
    BLUE = '\033[94m'      # Borders
    CYAN = '\033[96m'      # Info
    SUCCESS = '\033[92m'   # Green
    ERROR = '\033[91m'     # Red
    WARNING = '\033[93m'   # Yellow
    TEXT = '\033[97m'      # White
    DIM = '\033[2m'        # Faint text
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def clearScreen():
    """ Clears the console window to keep the UI clean """
    os.system('cls' if os.name == 'nt' else 'clear')

def pauseScreen():
    """ Keeps the message on screen until the user is ready """
    try:
        print("\n" + Colors.DIM + " " + "─"*58 + Colors.RESET)
    except UnicodeEncodeError:
        print("\n" + Colors.DIM + " " + "-"*58 + Colors.RESET)
    print(Colors.CYAN + " " + Colors.BOLD + ">>" + Colors.RESET + Colors.TEXT + " Press " + Colors.BOLD + "ENTER" + Colors.RESET + " to return to menu..." + Colors.RESET)
    input()

def renderHeader(registry):
    """ Renders a persistent system header """
    kiosk_id = registry.getConfig("KIOSK_ID") or "UNKNOWN"
    location = registry.getConfig("LOCATION") or "OFFLINE"
    curr_time = time.strftime("%H:%M:%S")
    
    header = f" {Colors.CYAN}{Colors.BOLD}AURA OS{Colors.RESET} {Colors.DIM}|{Colors.RESET} {Colors.TEXT}ID: {Colors.HEADER}{kiosk_id}{Colors.RESET} {Colors.DIM}|{Colors.RESET} {Colors.TEXT}LOC: {Colors.HEADER}{location}{Colors.RESET} {Colors.DIM}|{Colors.RESET} {Colors.TEXT}TIME: {Colors.CYAN}{curr_time}{Colors.RESET}"
    print("\n" + header)
    try:
        print(" " + Colors.DIM + "═"*75 + Colors.RESET + "\n")
    except UnicodeEncodeError:
        print(" " + Colors.DIM + "="*75 + Colors.RESET + "\n")

def showProgress(message, duration=1.2):
    """ List of characters that create the 'spinning' effect """
    spinner = ["|", "/", "-", "\\"]
    
    end_time = time.time() + duration
    idx = 0
    while time.time() < end_time:

        """ Move to the beginning of the line each time """
        print(f"\r {Colors.HEADER}{spinner[idx % len(spinner)]} {message}...", end="", flush=True)
        time.sleep(0.08)
        idx += 1
    
    """ Success message after check """
    print(f"\r {Colors.SUCCESS}[OK] {message} Done!{Colors.RESET}")

def drawBox(title, lines):    
    width = 60

    try:
        # Try printing with premium box characters
        print(Colors.BLUE + "╔" + "═"*(width-2) + "╗")
        print("║ " + Colors.HEADER + Colors.BOLD + title.center(width-4) + Colors.RESET + Colors.BLUE + " ║")
        print("╠" + "═"*(width-2) + "╣")
        for line in lines:
            print("║ " + Colors.TEXT + line.ljust(width-4) + Colors.RESET + Colors.BLUE + " ║")
        print("╚" + "═"*(width-2) + "╝" + Colors.RESET)
    except UnicodeEncodeError:
        # Fallback for older terminals
        print(Colors.BLUE + "+" + "-"*(width-2) + "+")
        print("| " + Colors.HEADER + Colors.BOLD + title.center(width-4) + Colors.RESET + Colors.BLUE + " |")
        print("+" + "-"*(width-2) + "+")
        for line in lines:
            print("| " + Colors.TEXT + line.ljust(width-4) + Colors.RESET + Colors.BLUE + " |")
        print("+" + "-"*(width-2) + "+" + Colors.RESET)

""" Display the inventory from products """
def strip_ansi(text):
    import re
    return re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])').sub('', text)

def pad_ansi(text, width, align='left'):
    plain = strip_ansi(text)
    diff = width - len(plain)
    if diff <= 0: return text
    if align == 'left': return text + (' ' * diff)
    if align == 'right': return (' ' * diff) + text
    if align == 'center':
        left = diff // 2
        right = diff - left
        return (' ' * left) + text + (' ' * right)
    return text

def displayInventory(products):
    """ 
    Displays the state-of-the-art Aura Kiosk Dashboard with perfect alignment.
    """
    mapping = {}
    idx = 1
    
    # Grid Config (Content Widths)
    W_REF   = 5
    W_NAME  = 30
    W_VAL   = 12
    W_STOCK = 38
    
    # Border Templates
    top    = f" ╔{'═'*W_REF}╦{'═'*W_NAME}╦{'═'*W_VAL}╦{'═'*W_STOCK}╗"
    header = f" ╠{'═'*W_REF}╬{'═'*W_NAME}╬{'═'*W_VAL}╬{'═'*W_STOCK}╣"
    sep    = f" ╟{'─'*W_REF}╫{'─'*W_NAME}╫{'─'*W_VAL}╫{'─'*W_STOCK}╢"
    bottom = f" ╚{'═'*W_REF}╩{'═'*W_NAME}╩{'═'*W_VAL}╩{'═'*W_STOCK}╝"

    try:
       
        print(Colors.BLUE + top)
        
        h_ref   = pad_ansi(f"{Colors.CYAN}REF", W_REF, 'center')
        h_name  = pad_ansi(f"{Colors.CYAN}IDENTIFIER", W_NAME, 'center')
        h_val   = pad_ansi(f"{Colors.CYAN}VALUATION", W_VAL, 'center')
        h_stock = pad_ansi(f"{Colors.CYAN}STOCK CAPACITY / STATUS", W_STOCK, 'center')
        
        print(f" {Colors.BLUE}║{h_ref}{Colors.BLUE}║{h_name}{Colors.BLUE}║{h_val}{Colors.BLUE}║{h_stock}{Colors.BLUE}║")
        print(Colors.BLUE + header)
        
        for name, prod in products.items():
            mapping[str(idx)] = name
            
            price_str = f"Rs.{prod.getPrice():,.2f}"
            stock_val = prod.getAvailableStock()
            
            # Stock Logic
            stock_color = Colors.SUCCESS
            status_text = "STABLE"
            if stock_val <= 0:
                stock_color, status_text = Colors.ERROR, "EMPTY "
            elif stock_val < 5:
                stock_color, status_text = Colors.WARNING, "LOW   "
            
            # Progress Bar (10 segments)
            filled = min(10, int((stock_val / 20) * 10))
            bar = f"{stock_color}{'█' * filled}{Colors.DIM}{'░' * (10-filled)}{Colors.RESET}"
            stock_status = f"{stock_color}[{status_text}]{Colors.RESET} {bar} {stock_color}{stock_val:>2} units{Colors.RESET}"
            
            is_bundle = isinstance(prod, ProductBundle)
            display_name = name.upper()
            
            if is_bundle:
                icon = f"{Colors.HEADER}⬢ {Colors.RESET}"
                item_text = f"{icon}{Colors.HEADER}{Colors.BOLD}{display_name}{Colors.RESET}"
            else:
                icon = f"{Colors.CYAN}● {Colors.RESET}"
                item_text = f"{icon}{Colors.TEXT}{display_name}{Colors.RESET}"
            
            # Row Printing
            c_ref   = pad_ansi(f"  {Colors.BOLD}{idx:<2}{Colors.RESET}", W_REF)
            c_name  = pad_ansi(f" {item_text}", W_NAME)
            c_val   = pad_ansi(f" {Colors.TEXT}{price_str:>10} ", W_VAL)
            c_stock = pad_ansi(f" {stock_status}", W_STOCK)
            
            print(f" {Colors.BLUE}║{c_ref}{Colors.BLUE}║{c_name}{Colors.BLUE}║{c_val}{Colors.BLUE}║{c_stock}{Colors.BLUE}║")
            
            # Bundle Tree
            if is_bundle:
                items = prod.getItems()
                for i, sub in enumerate(items):
                    conn = "╠═" if i < len(items) - 1 else "╚═"
                    sub_text = f" {Colors.DIM}  {conn} {sub.getName().upper()}{Colors.RESET}"
                    t_name = pad_ansi(sub_text, W_NAME)
                    t_ref  = pad_ansi("", W_REF)
                    t_val  = pad_ansi("", W_VAL)
                    t_stock = pad_ansi("", W_STOCK)
                    print(f" {Colors.BLUE}║{t_ref}{Colors.BLUE}║{t_name}{Colors.BLUE}║{t_val}{Colors.BLUE}║{t_stock}{Colors.BLUE}║")

            if idx < len(products):
                print(Colors.BLUE + sep)
            idx += 1
        
        print(Colors.BLUE + bottom + Colors.RESET)
        
    

    except UnicodeEncodeError:
        # Fallback
        print(f"\n --- CATALOG VIEW ---")
        print(Colors.BLUE + " +-----+-------------------------+------------+----------------------+")
        for name, prod in products.items():
            mapping[str(idx)] = name
            print(f" | {idx:<3} | {name.upper():<23} | Rs.{prod.getPrice():>7.2f} | {prod.getAvailableStock():>2} units |")
            idx += 1
        print(" +-----+-------------------------+------------+----------------------+" + Colors.RESET)
    
    return mapping
        
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
    print(Colors.BOLD + " --- QUICK SELECTION CATALOG --- " + Colors.RESET)
    mapping = displayInventory(products)

    ref = input(f"\n {Colors.CYAN}Enter Product Reference (1-{len(mapping)}):{Colors.RESET} ").strip()
    name = mapping.get(ref)
    item = products.get(name)
    
    if not item:
        print(Colors.ERROR + " ! Invalid reference selection." + Colors.RESET)
        pauseScreen()
        return

    try:
        print(f" Selected: {Colors.BOLD}{name.title()}{Colors.RESET}")
        qty = int(input(f" {Colors.CYAN}Enter quantity:{Colors.RESET} "))
    except ValueError:
        print(Colors.ERROR + " ! Please enter a valid number." + Colors.RESET)
        pauseScreen()
        return

    if qty > item.getAvailableStock():
        print(Colors.ERROR + " ! Not enough stock available." + Colors.RESET)
        pauseScreen()
        return

    method = paymentChoice()
    clearScreen()
    showProgress(f"Processing {method} Authorization")
    
    interface.purchaseItem(item, qty, method)
    print(Colors.SUCCESS + f"\n [SUCCESS] {qty}x {name.title()} dispensed." + Colors.RESET)
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
    print(Colors.BOLD + " --- RESTOCK MANAGEMENT --- " + Colors.RESET)
    mapping = displayInventory(products)
    
    ref = input(f"\n {Colors.CYAN}Select Item to Restock (1-{len(mapping)}):{Colors.RESET} ").strip()
    name = mapping.get(ref)
    item = products.get(name)
    
    if not item:
        print(Colors.ERROR + " ! Product not found." + Colors.RESET)
        pauseScreen()
        return

    try:
        print(f" Restocking: {Colors.BOLD}{name.title()}{Colors.RESET}")
        qty = int(input(f" {Colors.CYAN}Quantity to add:{Colors.RESET} "))
    except ValueError:
        print(Colors.ERROR + " ! Please enter a numeric value." + Colors.RESET)
        pauseScreen()
        return

    interface.restockInventory(item, qty)
    print(Colors.SUCCESS + f" [RESTOCK OK] {name.title()} inventory updated." + Colors.RESET)
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
    # 1. Setup Singleton Registry
    registry = CentralRegistry()
    registry.setConfig("KIOSK_ID", "AURA-001")
    registry.setConfig("LOCATION", "Main Hall - Floor 1")

    # 2. Setup Inventory System (Real Subject)
    inventory_real = InventorySystem()
    
    # Load individual products
    inventory_real.addProduct("milk",  SimpleProduct(ProductModel("P1", "milk", 50.0, 10)))
    inventory_real.addProduct("bread", SimpleProduct(ProductModel("P2", "bread", 30.0, 5)))
    inventory_real.addProduct("eggs",  SimpleProduct(ProductModel("P3", "eggs", 10.0, 20)))

    # Create a Product Bundle (Composite Pattern)
    # 10% discount for buying the combo
    breakfast_pack = ProductBundle("Breakfast Combo", discount=0.10) 
    breakfast_pack.add(inventory_real.getProduct("milk"))
    breakfast_pack.add(inventory_real.getProduct("bread"))
    breakfast_pack.add(inventory_real.getProduct("eggs"))
    
    # Add the bundle itself to the inventory
    inventory_real.addProduct("breakfast combo", breakfast_pack)

    # 3. Wrap in Security Proxy (Proxy Pattern)
    inventory_proxy = SecureInventoryProxy(inventory_real, role="STAFF")

    # 4. Setup Payment and Core
    payment_sys = PaymentSystem()
    core = KioskCoreSystem(inventorySystem=inventory_proxy, paymentSystem=payment_sys)
    
    # Register this kiosk instance globally
    registry.registerKiosk("AURA-001", core)

    # 5. Initialize Interface (Facade)
    interface = KioskInterface(core)

    welcomeScreen()

    # Create a mapping for legacy UI compatibility if needed, 
    # but we'll use the proxy's internal items for display
    inventory_items = inventory_real._items 

    while True:
        clearScreen()
        renderHeader(registry)
        
        drawBox("ACCESS MAIN TERMINAL", [
            " [1]  Quick Purchase",
            " [2]  Process Refund",
            " [3]  Restock Management",
            " [4]  System Diagnostics",
            " [5]  Power Down System"
        ])
        
        print(f"\n {Colors.CYAN}Selection{Colors.RESET} {Colors.DIM}>>{Colors.RESET} ", end="")
        choice = input().strip()

        if choice == "1":
            purchaseFlow(interface, inventory_items)
        elif choice == "2":
            refundFlow(interface)
        elif choice == "3":
            restockFlow(interface, inventory_items)
        elif choice == "4":
            diagnosticsFlow(core)
        elif choice == "5":
            clearScreen()
            drawBox("SHUTDOWN SEQUENCE", [
                "Cleaning up subsystems...",
                "Closing secure logs...",
                "Powering Down..."
            ])
            time.sleep(1.5)
            print(Colors.SUCCESS + " [SYSTEM] Offline. Goodbye!" + Colors.RESET)
            break
        else:
            print(f" {Colors.ERROR}! Invalid option. Please use 1-5.{Colors.RESET}")
            time.sleep(1)

runKiosk()