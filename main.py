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

from hardware.interfaces.hardwareAbstraction import HardwareAbstraction
from hardware.dispensers.spiralDispenser import SpiralDispenser

from monitoring.monitoring_system import MonitoringSystem
from persistence.persistenceLayer import PersistentLayer
from core.security.technicalSecurityProxy import TechnicalSecurityProxy

# Import Modules
from admin.admin_terminal import adminFlow
from factory.foodKioskFactory import FoodKioskFactory
from factory.pharmacyKioskFactory import PharmacyKioskFactory
from factory.techGearFactory import TechGearFactory
import os
import time
from utils.colors import Colors
from hardware.modules.solarModule import SolarModule
from hardware.modules.networkModule import NetworkModule
from hardware.modules.refrigerationUnit import RefrigerationUnit
from hardware.dispensers.roboticDispenser import RoboticDispenser


# Colors class was here


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
    kiosk_type = registry.getConfig("TYPE") or "CORE"
    curr_time = time.strftime("%H:%M:%S")
    
    header = f" {Colors.HEADER}{kiosk_type}{Colors.RESET} {Colors.DIM}|{Colors.RESET} {Colors.TEXT}ID: {Colors.CYAN}{kiosk_id}{Colors.RESET} {Colors.DIM}|{Colors.RESET} {Colors.TEXT}LOC: {Colors.CYAN}{location}{Colors.RESET} {Colors.DIM}|{Colors.RESET} {Colors.TEXT}TIME: {Colors.CYAN}{curr_time}{Colors.RESET}"
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

def drawBox(title, lines, color=Colors.BLUE):
    width = 62
    print(color + " ╔" + "═"*(width-2) + "╗")
    print(f" ║{Colors.BOLD}{pad_ansi(title, 60, 'center')}{Colors.RESET}{color}║")
    print(" ╠" + "═"*(width-2) + "╣")
    for line in lines:
        print(f" ║ {pad_ansi(line, 58, 'left')} ║")
    print(" ╚" + "═"*(width-2) + "╝" + Colors.RESET)

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
    showProgress("Checking Hardware (SpiralDispenser)")
    showProgress("Activating Monitoring System (Observer)")
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
        print("Refunding last transaction...")
    except ValueError:
        print(Colors.ERROR + " Please enter a valid number." + Colors.RESET)
        pauseScreen()
        return

    method = paymentChoice()
    showProgress("Contacting Bank for Refund")
    interface.refundTransaction(method)
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

# adminFlow was moved to admin/admin_terminal.py

def diagnosticsFlow(core):
    clearScreen()
    print(f"\n {Colors.CYAN}{Colors.BOLD}❖ SYSTEM DIAGNOSTICS ENGINE{Colors.RESET}")
    print(f" {Colors.DIM}─" + "─"*50 + Colors.RESET)
    
    # Core Status
    status = core.getSystemStatus()
    status_color = Colors.SUCCESS if status == "ACTIVE" else Colors.ERROR
    
    # Hardware Status (Step 3: Bridge)
    hw_info = core.hardwareSystem.getStatus() if core.hardwareSystem else {"dispenser": "NONE", "motorRunning": False}
    motor_status = f"{Colors.SUCCESS}ONLINE{Colors.RESET}" if hw_info['motorRunning'] else f"{Colors.DIM}IDLE{Colors.RESET}"
    
    drawBox("DIAGNOSTIC REPORT", [
        f" System Status:  {status_color}{status}{Colors.RESET}",
        f" Hardware ID:    {Colors.HEADER}HW-BRG-2024{Colors.RESET}",
        f" Dispenser:      {Colors.CYAN}{hw_info['dispenser']}{Colors.RESET}",
        f" Motor Module:   {motor_status}",
        f" Comm History:   {len(core.getCommandHistory())} executed",
        f" System Alerts:  {len(MonitoringSystem.getAlerts())} recorded",
    ])
    
    # Show recent alerts in diagnostics
    alerts = MonitoringSystem.getAlerts()
    if alerts:
        print(f"\n {Colors.WARNING}RECENT SYSTEM ALERTS:{Colors.RESET}")
        for alert in alerts[-3:]: # Show last 3
            print(f" {Colors.DIM}>> {alert}{Colors.RESET}")
    
    pauseScreen()
def saveCurrentInventory(inventory_items, filename="inventory.json"):
    """ Helper to save inventory to PersistentLayer """
    data = {"products": {}, "bundles": {}}
    for name, item in inventory_items.items():
        if isinstance(item, SimpleProduct):
            data["products"][name] = {
                "product_id": item.model.product_id,
                "name": item.model.name,
                "price": item.model.price,
                "stock": item.model.stock
            }
        elif isinstance(item, ProductBundle):
            item_keys = []
            for sub in item.getItems():
                for k, v in inventory_items.items():
                    if v == sub:
                        item_keys.append(k)
                        break
            
            data["bundles"][name] = {
                "name": item.getName(),
                "discount": item._discount,
                "items": item_keys
            }
    PersistentLayer.saveInventoryState(data, filename)

def loadInventoryIntoSystem(inventory_system, filename="inventory.json"):
    """ Helper to load inventory from PersistentLayer """
    data = PersistentLayer.loadInventoryState(filename)
    if not data or "products" not in data:
        return False
        
    # 1. Load Products
    for name, details in data["products"].items():
        model = ProductModel(
            details['product_id'], 
            details['name'], 
            details['price'], 
            details['stock']
        )
        inventory_system.addProduct(name, SimpleProduct(model))
    
    # 2. Load Bundles (if any)
    if "bundles" in data:
        for b_id, b_details in data["bundles"].items():
            bundle = ProductBundle(b_details['name'], b_details['discount'])
            for item_key in b_details['items']:
                prod = inventory_system.getProduct(item_key)
                if prod:
                    bundle.add(prod)
            inventory_system.addProduct(b_id, bundle)
            
    return True

def hardwareSimulationMenu(core):
    """
    TECHNICAL HARDWARE SIMULATION
    Manual control over decorators and dispensers.
    """
    while True:
        clearScreen()
        drawBox("HARDWARE SIMULATION CONTROL", [
            "Configure physical modules and active extensions:",
            " [1]  Attach Refrigeration Unit (Cooling)",
            " [2]  Attach Solar Energy Module",
            " [3]  Attach 5G Network Link",
            " [4]  Swap Dispenser Mechanism",
            " [5]  Clear All Extensions",
            " [6]  Return to Main Menu"
        ])
        
        # Show active modules
        active = core.getModuleStatuses()
        if active:
            print(f"\n {Colors.SUCCESS}Active Extensions:{Colors.RESET}")
            for k, v in active.items():
                print(f"  - {k.capitalize()}: {v}")
        
        choice = input(f"\n {Colors.CYAN}Selection >> {Colors.RESET}").strip()
        
        if choice == "1":
            core.attachModule(RefrigerationUnit(core.top_module))
        elif choice == "2":
            core.attachModule(SolarModule(core.top_module))
        elif choice == "3":
            core.attachModule(NetworkModule(core.top_module))
        elif choice == "4":
            clearScreen()
            drawBox("DISPENSER SELECTION", [
                "Select hardware mechanism to mount:",
                " [1]  Spiral (Standard Vending)",
                " [2]  Robotic Arm (Precision)",
                " [3]  Conveyor Belt (Bulk)"
            ])
            d_choice = input(f"\n {Colors.CYAN}Mechanism >> {Colors.RESET}").strip()
            if d_choice == "1": core.hardwareSystem.swapDispenser(SpiralDispenser())
            elif d_choice == "2": core.hardwareSystem.swapDispenser(RoboticDispenser())
            elif d_choice == "3": # Need to import or use a default
                from hardware.dispensers.conveyorDispenser import ConveyorDispenser
                core.hardwareSystem.swapDispenser(ConveyorDispenser())
        elif choice == "5":
            core.top_module = None
            print(f" {Colors.WARNING}All decorators removed.{Colors.RESET}")
            time.sleep(1)
        elif choice == "6":
            break

def runKiosk():
    # --- BOOT SCREEN & FACTORY SELECTION ---
    welcomeScreen()
    
    clearScreen()
    drawBox("SYSTEM CONFIGURATION", [
        "Please select the Kiosk Application Type:",
        " [1]  Food & Beverage (Spiral Dispenser)",
        " [2]  Medical Pharmacy (Robotic Arm)",
        " [3]  Cyber-Tech Gear (Conveyor Belt)"
    ])
    
    f_choice = input(f"\n {Colors.CYAN}Application Selection >> {Colors.RESET}").strip()
    if f_choice == "2":
        factory = PharmacyKioskFactory()
    elif f_choice == "3":
        factory = TechGearFactory()
    else:
        factory = FoodKioskFactory()
        
    kiosk_type_label = factory.getKioskType()
    
    # Map kiosk type to specific inventory file
    inv_map = {
        "Aura Food & Beverage Kiosk": "inventory_food.json",
        "Aura Medical Pharmacy Kiosk": "inventory_pharmacy.json",
        "Aura Cyber-Tech Hub": "inventory_tech.json"
    }
    inventory_file = inv_map.get(kiosk_type_label, "inventory_default.json")
    
    # --- SUB-SYSTEM INITIALIZATION ---
    # Step 1: Singleton Registry
    registry = CentralRegistry()
    
    # Step 6: Persistence Initialization
    inventory_real = InventorySystem()
    
    # Try to load from DB, fallback to factory defaults if empty
    if not loadInventoryIntoSystem(inventory_real, inventory_file):
        print(f"{Colors.WARNING} [INFO] Initializing factory data for {kiosk_type_label}...{Colors.RESET}")
        
        # Get factory data (NEW!)
        data = factory.getDefaultInventory()
        
        # Load products from factory data
        for k, p in data["products"].items():
            inventory_real.addProduct(k, SimpleProduct(ProductModel(p["id"], p["name"], p["price"], p["stock"])))
            
        # Load bundles from factory data
        for k, b in data["bundles"].items():
            bundle = ProductBundle(b["name"], b["discount"])
            for item_key in b["items"]:
                prod = inventory_real.getProduct(item_key)
                if prod: bundle.add(prod)
            inventory_real.addProduct(k, bundle)

        # Save the new database immediately
        saveCurrentInventory(inventory_real._items, inventory_file)
    else:
        print(f"{Colors.SUCCESS} [DB] {kiosk_type_label} state restored from {inventory_file}.{Colors.RESET}")

    # Step 4: Monitoring (Observer Pattern)
    monitor = MonitoringSystem()
    monitor.subscribe("LOW_STOCK", lambda src, det: print(f"{Colors.ERROR}\n [ALERT] {det} (Triggered by {src}){Colors.RESET}"))
    
    proxy = SecureInventoryProxy(
        inventory_real, 
        monitor=monitor, 
        on_change=lambda: saveCurrentInventory(inventory_real._items, inventory_file)
    )

    # Step 3: Hardware Bridge (PROVISIONED BY FACTORY)
    dispenser = factory.createDispenser()
    hardware = HardwareAbstraction(dispenser)

    # Core System Assembly
    payment = PaymentSystem()
    core = KioskCoreSystem(
        inventorySystem=proxy,
        paymentSystem=payment,
        hardwareSystem=hardware,
        kioskType=kiosk_type_label
    )

    # Register this kiosk instance globally
    registry.setConfig("KIOSK_ID", "AURA-001")
    registry.setConfig("LOCATION", "Main Hall - Floor 1")
    registry.setConfig("TYPE", kiosk_type_label)
    registry.registerKiosk("AURA-001", core)

    # 5. Initialize Interface (Facade)
    interface = KioskInterface(core)
    inventory_items = inventory_real._items 

    # Removed second welcomeScreen call

    while True:
        clearScreen()
        renderHeader(registry)
        
        drawBox("ACCESS MAIN TERMINAL", [
            " [1]  Quick Purchase",
            " [2]  Process Refund",
            " [3]  System Diagnostics",
            " [4]  Admin Terminal (Restricted)",
            " [5]  Hardware Simulation (Technical)",
            " [6]  Power Down System"
        ])
        
        print(f"\n {Colors.CYAN}Selection{Colors.RESET} {Colors.DIM}>>{Colors.RESET} ", end="")
        choice = input().strip()

        if choice == "1":
            purchaseFlow(interface, inventory_items)
        elif choice == "2":
            refundFlow(interface)
        elif choice == "3":
            diagnosticsFlow(core)
        elif choice == "4":
            pin = input(f"\n {Colors.WARNING} Enter ADMIN PIN:{Colors.RESET} ").strip()
            if pin == "1234":
                adminFlow(
                    inventory_real, 
                    registry, 
                    interface, 
                    save_callback=lambda: saveCurrentInventory(inventory_items, inventory_file)
                )
            else:
                print(f" {Colors.ERROR} Access Denied.{Colors.RESET}")
                time.sleep(1)
        elif choice == "5":
            security = TechnicalSecurityProxy(hardwareSimulationMenu)
            security.authenticate_and_run(core)
        elif choice == "6":
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