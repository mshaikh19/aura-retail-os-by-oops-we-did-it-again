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

# Import Modules
from admin.adminTerminal import adminFlow
from factory.foodKioskFactory import FoodKioskFactory
from factory.pharmacyKioskFactory import PharmacyKioskFactory
from factory.techGearFactory import TechGearFactory
from core.security.protectionProxy import TechnicianSecurityProxy
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

def renderHeader(registry, width=80):
    """ Renders a persistent system header centered on screen """
    kiosk_id = registry.getConfig("KIOSK_ID") or "UNKNOWN"
    location = registry.getConfig("LOCATION") or "OFFLINE"
    kiosk_type = registry.getConfig("TYPE") or "CORE"
    curr_time = time.strftime("%H:%M:%S")
    
    header = f"{Colors.HEADER}{kiosk_type}{Colors.RESET} {Colors.DIM}|{Colors.RESET} {Colors.TEXT}ID: {Colors.CYAN}{kiosk_id}{Colors.RESET} {Colors.DIM}|{Colors.RESET} {Colors.TEXT}LOC: {Colors.CYAN}{location}{Colors.RESET} {Colors.DIM}|{Colors.RESET} {Colors.TEXT}TIME: {Colors.CYAN}{curr_time}{Colors.RESET}"
    print("\n" + centerLine(header, width))
    try:
        print(centerLine(Colors.DIM + "═"*75 + Colors.RESET, width) + "\n")
    except UnicodeEncodeError:
        print(centerLine(Colors.DIM + "="*75 + Colors.RESET, width) + "\n")

def showProgress(message, task_func=None, duration=0.8, width=80):
    """ Restored classic progress spinner with centering """
    spinner = ["|", "/", "-", "\\"]
    
    idx = 0
    start_time = time.time()
    
    result = None
    if task_func:
        # Run the actual task
        result = task_func()
    
    # Ensure a minimum duration for visual impact
    while time.time() - start_time < duration:
        line = f"{Colors.HEADER}{spinner[idx % len(spinner)]}{Colors.RESET} {message}..."
        print(f"\r{centerLine(line, width)}", end="", flush=True)
        time.sleep(0.08)
        idx += 1
    
    success_line = f"{Colors.SUCCESS}[OK] {message} Done!{Colors.RESET}"
    print(f"\r{centerLine(success_line, width)}")
    return result

def centerLine(text, width=80):
    """ Helper to center text while ignoring ANSI color codes """
    import re
    plain = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])').sub('', text)
    padding = max(0, (width - len(plain)) // 2)
    return (" " * padding) + text

def printLogo():
    width = 80
    lines = [
        "█████  ██   ██ ██████   █████ ",
        "██   ██ ██   ██ ██   ██ ██   ██",
        "███████ ██   ██ ██████  ███████",
        "██   ██ ██   ██ ██   ██ ██   ██",
        "██   ██  █████  ██   ██ ██   ██"
    ]
    print(f"\n{Colors.CYAN}")
    for line in lines:
        print(centerLine(line, width))
    print(f"{Colors.RESET}")



def drawBox(title, lines, screen_width=80):    
    width = 60
    indent = " " * ((screen_width - width) // 2)

    try:
        # Try printing with premium box characters
        print(indent + Colors.BLUE + "╔" + "═"*(width-2) + "╗")
        print(indent + "║ " + Colors.HEADER + Colors.BOLD + title.center(width-4) + Colors.RESET + Colors.BLUE + " ║")
        print(indent + "╠" + "═"*(width-2) + "╣")
        for line in lines:
            print(indent + "║ " + Colors.TEXT + line.ljust(width-4) + Colors.RESET + Colors.BLUE + " ║")
        print(indent + "╚" + "═"*(width-2) + "╝" + Colors.RESET)
    except UnicodeEncodeError:
        # Fallback for older terminals
        print(indent + Colors.BLUE + "+" + "-"*(width-2) + "+")
        print(indent + "| " + Colors.HEADER + Colors.BOLD + title.center(width-4) + Colors.RESET + Colors.BLUE + " |")
        print(indent + "+" + "-"*(width-2) + "+")
        for line in lines:
            print(indent + "| " + Colors.TEXT + line.ljust(width-4) + Colors.RESET + Colors.BLUE + " |")
        print(indent + "+" + "-"*(width-2) + "+" + Colors.RESET)

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

def displayInventory(products, screen_width=80):
    """ 
    Displays the state-of-the-art Aura Kiosk Dashboard with perfect centering and alignment.
    """
    mapping = {}
    idx = 1
    
    # Adjusted Grid Config (Fits 80 chars with padding)
    W_REF   = 4
    W_NAME  = 25
    W_VAL   = 10
    W_STOCK = 32
    
    table_width = W_REF + W_NAME + W_VAL + W_STOCK + 5
    indent = " " * ((screen_width - table_width) // 2)
    
    # Border Templates
    top    = f"{indent}╔{'═'*W_REF}╦{'═'*W_NAME}╦{'═'*W_VAL}╦{'═'*W_STOCK}╗"
    header = f"{indent}╠{'═'*W_REF}╬{'═'*W_NAME}╬{'═'*W_VAL}╬{'═'*W_STOCK}╣"
    sep    = f"{indent}╟{'─'*W_REF}╫{'─'*W_NAME}╫{'─'*W_VAL}╫{'─'*W_STOCK}╢"
    bottom = f"{indent}╚{'═'*W_REF}╩{'═'*W_NAME}╩{'═'*W_VAL}╩{'═'*W_STOCK}╝"

    try:
       
        print(Colors.BLUE + top)
        
        h_ref   = pad_ansi(f"{Colors.CYAN}REF", W_REF, 'center')
        h_name  = pad_ansi(f"{Colors.CYAN}IDENTIFIER", W_NAME, 'center')
        h_val   = pad_ansi(f"{Colors.CYAN}VALUATION", W_VAL, 'center')
        h_stock = pad_ansi(f"{Colors.CYAN}STOCK CAPACITY / STATUS", W_STOCK, 'center')
        
        print(f"{indent}{Colors.BLUE}║{h_ref}{Colors.BLUE}║{h_name}{Colors.BLUE}║{h_val}{Colors.BLUE}║{h_stock}{Colors.BLUE}║")
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
            
            # Progress Bar (8 segments for smaller table)
            filled = min(8, int((stock_val / 20) * 8))
            bar = f"{stock_color}{'█' * filled}{Colors.DIM}{'░' * (8-filled)}{Colors.RESET}"
            stock_status = f"{stock_color}[{status_text}]{Colors.RESET} {bar} {stock_color}{stock_val:>2}u{Colors.RESET}"
            
            is_bundle = isinstance(prod, ProductBundle)
            display_name = name.upper()
            
            if is_bundle:
                icon = f"{Colors.HEADER}⬢ {Colors.RESET}"
                item_text = f"{icon}{Colors.HEADER}{Colors.BOLD}{display_name}{Colors.RESET}"
            else:
                icon = f"{Colors.CYAN}● {Colors.RESET}"
                item_text = f"{icon}{Colors.TEXT}{display_name}{Colors.RESET}"
            
            # Row Printing
            c_ref   = pad_ansi(f" {Colors.BOLD}{idx:<2}{Colors.RESET}", W_REF)
            c_name  = pad_ansi(f" {item_text}", W_NAME)
            c_val   = pad_ansi(f" {Colors.TEXT}{price_str:>8} ", W_VAL)
            c_stock = pad_ansi(f" {stock_status}", W_STOCK)
            
            print(f"{indent}{Colors.BLUE}║{c_ref}{Colors.BLUE}║{c_name}{Colors.BLUE}║{c_val}{Colors.BLUE}║{c_stock}{Colors.BLUE}║")
            
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
                    print(f"{indent}{Colors.BLUE}║{t_ref}{Colors.BLUE}║{t_name}{Colors.BLUE}║{t_val}{Colors.BLUE}║{t_stock}{Colors.BLUE}║")

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
    width = 80
    clearScreen()
    printLogo()
    
    print(centerLine(f"{Colors.BOLD}RETAIL OPERATING SYSTEM{Colors.RESET}", width))
    print(centerLine(f"{Colors.DIM}v4.2.0-STABLE | BUILD 2024.04{Colors.RESET}", width))
    print()
    
    print(centerLine(f"{Colors.CYAN}Welcome to the future of automated retail.{Colors.RESET}", width))
    time.sleep(0.5)
    
    print("\n" + centerLine(f"{Colors.BOLD}PRESS ENTER TO INITIALIZE{Colors.RESET}", width))
    input()

    # Perform real tasks for common subsystems
    print()
    registry = showProgress("Initializing Central Registry", lambda: CentralRegistry(), duration=0.6, width=width)
    inventory_real = showProgress("Mounting Secure Inventory Engine", lambda: InventorySystem(), duration=0.6, width=width)
    monitor = showProgress("Activating Monitoring System", lambda: MonitoringSystem(), duration=0.6, width=width)
    payment = showProgress("Initializing Payment Gateway API", lambda: PaymentSystem(), duration=0.6, width=width)
    showProgress("Opening Secure Gateway", duration=0.6, width=width)
    time.sleep(0.5)
    
    return registry, inventory_real, monitor, payment

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

    # Emergency Mode: restrict single transaction to max 2 units
    from registry.central_registry import CentralRegistry
    if CentralRegistry().getConfig("EMERGENCY_MODE"):
        if qty > 2:
            print(Colors.WARNING + " ! EMERGENCY MODE: Purchase limit is 2 units per transaction." + Colors.RESET)
            pauseScreen()
            return

    if qty > item.getAvailableStock():
        print(Colors.ERROR + " ! Not enough stock available." + Colors.RESET)
        pauseScreen()
        return

    method = paymentChoice()
    clearScreen()
    
    interface.purchaseItem(item, qty, method)
    showProgress(f"Processing {method} Authorization")
    print(Colors.SUCCESS + f"\n [SUCCESS] {qty}x {name.title()} dispensed." + Colors.RESET)
    pauseScreen()

def refundFlow(interface):
    width = 80
    clearScreen()
    printLogo()
    print(centerLine(f"{Colors.HEADER}◈ REFUND PROCESSING CENTER{Colors.RESET}", width))
    print(centerLine(f"{Colors.DIM}Standard reversal protocol v4.0{Colors.RESET}", width))
    print()

    # Pre-check: Is a refund even possible in this session?
    if not interface.isRefundAvailable():
        print(centerLine(f"{Colors.ERROR}[DENIED] No eligible transactions found in your current session.{Colors.RESET}", width))
        print(centerLine(f"{Colors.TEXT}Refunds are only available for items purchased in the active session.{Colors.RESET}", width))
        pauseScreen()
        return

    method = paymentChoice()
    
    # Process the refund
    clearScreen()
    printLogo()
    print(centerLine(f"{Colors.CYAN}Initiating Reversal Sequence...{Colors.RESET}", width))
    print()
    
    try:
        # The interface now returns True/False based on core execution
        success = interface.refundTransaction(method)
        
        if success:
            showProgress("Validating Transaction History", duration=0.6, width=width)
            showProgress("Contacting Bank for Reversal", duration=0.8, width=width)
            print("\n" + centerLine(f"{Colors.SUCCESS}[SUCCESS] The transaction has been fully reversed.{Colors.RESET}", width))
            print(centerLine(f"{Colors.TEXT}Funds will reflect in your {method} account shortly.{Colors.RESET}", width))
        else:
            # Error message is usually printed by the subsystems (PaymentSystem/Core)
            print("\n" + centerLine(f"{Colors.ERROR}[FAILED] Reversal could not be completed.{Colors.RESET}", width))
    except Exception as e:
        print("\n" + centerLine(f"{Colors.ERROR}[SYSTEM ERROR] {str(e)}{Colors.RESET}", width))

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
                "stock": item.model.stock,
                "required_module": getattr(item.model, "required_module", None)
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
            details['stock'],
            required_module=details.get('required_module')
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
    PROTECTED BY: TechnicianSecurityProxy
    """
    # 1. Protection Layer
    proxy = TechnicianSecurityProxy(core)
    
    clearScreen()
    print(f"\n {Colors.WARNING}{Colors.BOLD} [!] SECURITY PROTOCOL REQUIRED{Colors.RESET}")
    print(f" {Colors.DIM}This terminal is restricted to authorized field engineers.{Colors.RESET}")
    
    tech_id = input(f"\n {Colors.CYAN}Enter Technician ID: {Colors.RESET}").strip()
    if not proxy.authenticate(tech_id):
        return

    def save_hw_config():
        """ Local helper to sync HW modules to persistent config """
        modules = core.getActiveModuleNames()
        registry = CentralRegistry()
        registry.setConfig("ACTIVE_MODULES", modules)
        PersistentLayer.saveConfig(registry._config)

    # 2. Main Simulation Console
    while True:
        clearScreen()
        # High-Tech Header
        print(f" {Colors.HEADER}❖ FIELD SERVICE CONSOLE {Colors.RESET} {Colors.DIM}v4.2.0-STABLE{Colors.RESET}")
        print(f" {Colors.DIM}───────────────────────────────────────────────────────────{Colors.RESET}")
        
        # Live Hardware Feed
        active = proxy.getModuleStatuses()
        hw_type = type(core.hardwareSystem._dispenser).__name__
        
        print(f" {Colors.BOLD}PHYSICAL STACK:{Colors.RESET} {Colors.CYAN}{hw_type}{Colors.RESET}")
        print(f" {Colors.BOLD}ACTIVE EXTENSIONS:{Colors.RESET} ", end="")
        if not active:
            print(f"{Colors.DIM}None Detected{Colors.RESET}")
        else:
            print(", ".join([f"{Colors.SUCCESS}{k.upper()}{Colors.RESET}" for k in active.keys()]))
            
        print(f" {Colors.DIM}───────────────────────────────────────────────────────────{Colors.RESET}")

        drawBox("HARDWARE MAINTENANCE TOOLS", [
            " [1]  Engage Refrigeration Unit",
            " [2]  Deploy Solar Power Panels",
            " [3]  Initialize 5G Network Uplink",
            " [4]  Hot-Swap Dispenser Mechanism",
            " [5]  Toggle Product Slot Jam",
            " [6]  Decommission All Extensions",
            " [7]  Return to Primary Shell"
        ])
        
        choice = input(f"\n {Colors.CYAN}Technician >> {Colors.RESET}").strip()
        
        if choice == "1":
            proxy.attachModule(RefrigerationUnit(core.top_module))
            save_hw_config()
            time.sleep(0.5)
        elif choice == "2":
            proxy.attachModule(SolarModule(core.top_module))
            save_hw_config()
            time.sleep(0.5)
        elif choice == "3":
            proxy.attachModule(NetworkModule(core.top_module))
            save_hw_config()
            time.sleep(0.5)
        elif choice == "4":
            clearScreen()
            print(f"\n {Colors.WARNING} [!] WARNING: SUSPENDING DISPENSE OPERATIONS{Colors.RESET}")
            drawBox("MECH SELECTION", [
                " [1]  Spiral (Standard Vending)",
                " [2]  Robotic Arm (Precision)",
                " [3]  Conveyor Belt (Bulk)"
            ])
            d_choice = input(f"\n {Colors.CYAN}Select Mech >> {Colors.RESET}").strip()
            if d_choice == "1": proxy.swapDispenser(SpiralDispenser())
            elif d_choice == "2": proxy.swapDispenser(RoboticDispenser())
            elif d_choice == "3":
                from hardware.dispensers.conveyorDispenser import ConveyorDispenser
                proxy.swapDispenser(ConveyorDispenser())
            time.sleep(1)
        elif choice == "5":
            clearScreen()
            print(f"\n {Colors.HEADER}❖ JAM SIMULATION MODULE{Colors.RESET}")
            inventory_items = core.inventorySystem._inventory_system._items
            mapping = {}
            lines = []
            for i, name in enumerate(inventory_items.keys(), 1):
                mapping[str(i)] = name
                status = "JAMMED" if core.hardwareSystem.isProductJammed(name) else "CLEAR"
                lines.append(f" [{i}] {name.upper():<20} | {status}")
            
            drawBox("SELECT SLOT TO TOGGLE", lines)
            j_choice = input(f"\n {Colors.CYAN}Toggle Slot # >> {Colors.RESET}").strip()
            if j_choice in mapping:
                core.hardwareSystem.toggleProductJam(mapping[j_choice])
                time.sleep(1)
        elif choice == "6":
            proxy.clearExtensions()
            save_hw_config()
            time.sleep(1)
        elif choice == "7":
            break


def runKiosk():
    # --- BOOT SCREEN & INITIALIZATION ---
    registry, inventory_real, monitor, payment = welcomeScreen()
    
    # Step 0: Load Persistence Config for Presets
    config = PersistentLayer.loadConfig()
    f_choice = config.get("KIOSK_PRESET")

    if not f_choice:
        clearScreen()
        printLogo()
        drawBox("SYSTEM CONFIGURATION", [
            "Please select the Kiosk Application Type:",
            " [1]  Food & Beverage (Spiral Dispenser)",
            " [2]  Medical Pharmacy (Robotic Arm)",
            " [3]  Cyber-Tech Gear (Conveyor Belt)"
        ])
        
        f_choice = input(f"\n {Colors.CYAN}Application Selection >> {Colors.RESET}").strip()
        
        # Save selection for next boot
        config["KIOSK_PRESET"] = f_choice
        PersistentLayer.saveConfig(config)
    
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
    
    clearScreen()
    printLogo()
    print(f" {Colors.HEADER}❖ SYSTEM BOOT SEQUENCE - {kiosk_type_label.upper()}{Colors.RESET}")
    print(f" {Colors.DIM}───────────────────────────────────────────────────────────{Colors.RESET}\n")

    # Step 6: Load Inventory Data
    def load_logic():
        if not loadInventoryIntoSystem(inventory_real, inventory_file):
            data = factory.getDefaultInventory()
            for k, p in data["products"].items():
                inventory_real.addProduct(k, SimpleProduct(ProductModel(p["id"], p["name"], p["price"], p["stock"])))
            for k, b in data["bundles"].items():
                bundle = ProductBundle(b["name"], b["discount"])
                for item_key in b["items"]:
                    prod = inventory_real.getProduct(item_key)
                    if prod: bundle.add(prod)
                inventory_real.addProduct(k, bundle)
            saveCurrentInventory(inventory_real._items, inventory_file)
            return "FACTORY_INIT"
        return "DATABASE_RESTORED"

    status = showProgress(f"Syncing Catalog DB ({inventory_file})", load_logic)
    
    # Step 4: Configure Monitoring
    monitor.subscribe("LOW_STOCK", lambda src, det: print(f"{Colors.ERROR}\n [ALERT] {det} (Triggered by {src}){Colors.RESET}"))
    
    proxy = showProgress("Establishing Secure Inventory Proxy", 
        lambda: SecureInventoryProxy(
            inventory_real, 
            monitor=monitor, 
            on_change=lambda: saveCurrentInventory(inventory_real._items, inventory_file)
        )
    )

    # Step 3: Hardware Bridge
    dispenser = showProgress("Provisioning Dispenser Mechanism", lambda: factory.createDispenser())
    hardware = showProgress("Bridging Hardware Abstraction Layer", lambda: HardwareAbstraction(dispenser))
    registry.registerHardware(hardware)


    # Core System Assembly
    core = showProgress("Assembling Aura Core Kernel", 
        lambda: KioskCoreSystem(
            inventorySystem=proxy,
            paymentSystem=payment,
            hardwareSystem=hardware,
            kioskType=kiosk_type_label
        )
    )

    # Register this kiosk instance globally
    showProgress("Registering Kiosk Identity", 
        lambda: (
            registry.setConfig("KIOSK_ID", "AURA-001"),
            registry.setConfig("LOCATION", "Main Hall - Floor 1"),
            registry.setConfig("TYPE", kiosk_type_label),
            registry.registerKiosk("AURA-001", core)
        )
    )

    # Step 7: Initialize Session
    core.sessionManager.startSession(kiosk_id="AURA-001")

    # --- RESTORE PERSISTENT HARDWARE MODULES ---
    def restore_modules():
        saved_modules = registry.getConfig("ACTIVE_MODULES") or []
        for mod_name in saved_modules:
            if mod_name == "refrigeration": core.attachModule(RefrigerationUnit(core.top_module))
            elif mod_name == "solar": core.attachModule(SolarModule(core.top_module))
            elif mod_name == "network": core.attachModule(NetworkModule(core.top_module))
        return len(saved_modules)

    mod_count = showProgress("Restoring Hardware Extension Modules", restore_modules)

    # 5. Initialize Interface (Facade)
    interface = showProgress("Launching Kiosk Interface Facade", lambda: KioskInterface(core))
    inventory_items = inventory_real._items 

    print(f"\n {Colors.SUCCESS}███ BOOT SUCCESSFUL ███{Colors.RESET}")
    time.sleep(1)

    while True:
        clearScreen()
        renderHeader(registry)
        
        drawBox("ACCESS MAIN TERMINAL", [
            " [1]  Quick Purchase",
            " [2]  Process Refund",
            " [3]  System Diagnostics",
            " [4]  Management Console (Restricted)",
            " [5]  Power Down System"
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
            clearScreen()
            drawBox("SECURE OPERATIONS HUB", [
                "Select Authorization Node:",
                " [1]  Inventory & Asset Control",
                " [2]  Hardware Abstraction Node",
                " [3]  Exit Secure Shell"
            ])
            sub_choice = input(f"\n {Colors.CYAN}Access Level >> {Colors.RESET}").strip()
            
            if sub_choice == "1":
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
            elif sub_choice == "2":
                hardwareSimulationMenu(core)
            elif sub_choice == "3":
                continue
        elif choice == "5":
            # Safely close the active session
            core.sessionManager.endSession()
            
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