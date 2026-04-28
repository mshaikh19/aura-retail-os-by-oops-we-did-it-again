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
from registry.centralRegistry import CentralRegistry

from hardware.interfaces.hardwareAbstraction import HardwareAbstraction
from hardware.dispensers.spiralDispenser import SpiralDispenser

from monitoring.monitoringSystem import MonitoringSystem
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
    """ Clears the console window using both OS commands and ANSI resets """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    # Force ANSI clear to handle buffer-scrolling terminals
    print("\033[H\033[2J\033[3J", end="", flush=True)

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
    """ Minimalist retail-ready progress indicator """
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    idx = 0
    start_time = time.time()
    
    result = None
    if task_func:
        result = task_func()
    
    while time.time() - start_time < duration:
        line = f"{Colors.CYAN}{spinner[idx % len(spinner)]}{Colors.RESET} {Colors.DIM}{message}...{Colors.RESET}"
        print(f"\r{centerLine(line, width)}", end="", flush=True)
        time.sleep(0.08)
        idx += 1
    
    # Just clear the line when done, don't show technical [OK]
    print(f"\r{' '*width}\r", end="")
    return result

def strip_ansi(text):
    """ Removes ANSI escape sequences from a string to get its real length. """
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def centerLine(text, width=80):
    """ Helper to center text while ignoring ANSI color codes """
    plain = strip_ansi(text)
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



from utils.ui_utils import pad_ansi, strip_ansi, drawBox



def displayInventory(products, active_modules=None, screen_width=80):
    """ 
    Displays the state-of-the-art Aura Kiosk Dashboard with perfect centering and alignment.
    """
    mapping = {}
    idx = 1
    
    # Defined constants for layout
    W_REF = 5
    W_NAME = 26
    W_VAL = 14
    W_STOCK = 26
    table_width = W_REF + W_NAME + W_VAL + W_STOCK + 5
    tbl_indent = " " * ((screen_width - table_width) // 2)
    
    # High-Definition Border Templates
    top    = f"{tbl_indent}╔{'═'*W_REF}╦{'═'*W_NAME}╦{'═'*W_VAL}╦{'═'*W_STOCK}╗"
    header = f"{tbl_indent}╠{'═'*W_REF}╬{'═'*W_NAME}╬{'═'*W_VAL}╬{'═'*W_STOCK}╣"
    sep    = f"{tbl_indent}╟{'─'*W_REF}╫{'─'*W_NAME}╫{'─'*W_VAL}╫{'─'*W_STOCK}╢"
    bottom = f"{tbl_indent}╚{'═'*W_REF}╩{'═'*W_NAME}╩{'═'*W_VAL}╩{'═'*W_STOCK}╝"

    try:
        print(Colors.BLUE + top)
        
        h_ref   = pad_ansi(f" {Colors.CYAN}REF", W_REF, 'center')
        h_name  = pad_ansi(f" {Colors.CYAN}IDENTIFIER", W_NAME, 'center')
        h_val   = pad_ansi(f" {Colors.CYAN}VALUATION", W_VAL, 'center')
        h_stock = pad_ansi(f" {Colors.CYAN}STOCK CAPACITY / STATUS", W_STOCK, 'center')
        
        print(f"{tbl_indent}{Colors.BLUE}║{h_ref}{Colors.BLUE}║{h_name}{Colors.BLUE}║{h_val}{Colors.BLUE}║{h_stock}{Colors.BLUE}║")
        print(Colors.BLUE + header)
        
        active_modules = active_modules or []
        
        for name, prod in products.items():
            # Module Check
            req_mod = getattr(prod.model, "required_module", None) if not isinstance(prod, ProductBundle) else None
            is_available = not (req_mod and req_mod not in active_modules)

            mapping[str(idx)] = name
            price_str = f"Rs.{prod.getPrice():,.2f}"
            stock_val = prod.getAvailableStock()
            
            # Stock Logic
            stock_color = Colors.SUCCESS
            status_text = "STABLE"
            if not is_available:
                stock_color, status_text = Colors.DIM, "OFFLINE"
            elif stock_val <= 0:
                stock_color, status_text = Colors.ERROR, "EMPTY "
            elif stock_val < 5:
                stock_color, status_text = Colors.WARNING, "LOW   "
            
            # Progress Bar (8 segments)
            if is_available:
                filled = min(8, int((stock_val / 20) * 8))
                bar = f"{stock_color}{'█' * filled}{Colors.DIM}{'░' * (8-filled)}{Colors.RESET}"
                stock_status = f"{stock_color}[{status_text}]{Colors.RESET} {bar} {stock_color}{stock_val:>2}u{Colors.RESET}"
            else:
                stock_status = f"{Colors.DIM}[MODULE REQ: {req_mod.upper()}]{Colors.RESET}"

            is_bundle = isinstance(prod, ProductBundle)
            display_name = name.upper()
            
            if not is_available:
                item_text = f"{Colors.DIM}○ {display_name}{Colors.RESET}"
                price_str = f"{Colors.DIM}---{Colors.RESET}"
            elif is_bundle:
                item_text = f"{Colors.HEADER}⬢ {Colors.BOLD}{display_name}{Colors.RESET}"
            else:
                item_text = f"{Colors.CYAN}● {Colors.TEXT}{display_name}{Colors.RESET}"
            
            # Row Printing
            c_ref   = pad_ansi(f" {Colors.BOLD if is_available else Colors.DIM}{idx:<2}{Colors.RESET}", W_REF, 'center')
            c_name  = pad_ansi(f" {item_text}", W_NAME)
            c_val   = pad_ansi(f" {Colors.TEXT if is_available else Colors.DIM}{price_str:>8} ", W_VAL, 'center')
            c_stock = pad_ansi(f" {stock_status}", W_STOCK)
            
            print(f"{tbl_indent}{Colors.BLUE}║{c_ref}{Colors.BLUE}║{c_name}{Colors.BLUE}║{c_val}{Colors.BLUE}║{c_stock}{Colors.BLUE}║")
            
            # Bundle Tree
            if is_bundle and is_available:
                sub_items = prod.getItems()
                for i, sub in enumerate(sub_items):
                    conn = "╠═" if i < len(sub_items) - 1 else "╚═"
                    sub_text = f" {Colors.DIM}  {conn} {sub.getName().upper()}{Colors.RESET}"
                    t_name = pad_ansi(sub_text, W_NAME)
                    t_ref  = pad_ansi("", W_REF)
                    t_val  = pad_ansi("", W_VAL)
                    t_stock = pad_ansi("", W_STOCK)
                    print(f"{tbl_indent}{Colors.BLUE}║{t_ref}{Colors.BLUE}║{t_name}{Colors.BLUE}║{t_val}{Colors.BLUE}║{t_stock}{Colors.BLUE}║")
            
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
# Redundant welcomeScreen removed to unify boot flow

def paymentChoice(registry):
    """ Gets payment choice using an easy-to-understand menu with hardware validation """
    active_modules = registry.getConfig("ACTIVE_MODULES") or []
    has_network = "network" in [m.lower() for m in active_modules]

    clearScreen()
    
    upi_line = "1. UPI (Online QR)"
    card_line = "2. Credit/Debit Card"
    
    if not has_network:
        upi_line += f" {Colors.ERROR}[OFFLINE]{Colors.RESET}"
        card_line += f" {Colors.ERROR}[OFFLINE]{Colors.RESET}"

    drawBox("PAYMENT GATEWAY", [
        upi_line,
        card_line,
        "3. Digital Wallet",
        "",
        f" {Colors.DIM}Note: UPI/Card require active Network Module.{Colors.RESET}"
    ])
    
    while True:
        choice = input(f"\n {Colors.CYAN}Select Payment Method (1-3): {Colors.RESET}").strip()
        if choice == "1":
            if not has_network:
                print(f" {Colors.ERROR}! UPI unavailable. Please select another method.{Colors.RESET}")
                continue
            return "UPI"
        if choice == "2":
            if not has_network:
                print(f" {Colors.ERROR}! CARD unavailable. Please select another method.{Colors.RESET}")
                continue
            return "CARD"
        if choice == "3": 
            return "WALLET"
        print(f" {Colors.ERROR}! Invalid selection.{Colors.RESET}")

def purchaseFlow(interface, products):
    from registry.centralRegistry import CentralRegistry
    clearScreen()
    print(Colors.BOLD + " --- QUICK SELECTION CATALOG --- " + Colors.RESET)
    active_modules = CentralRegistry().getConfig("ACTIVE_MODULES") or []
    mapping = displayInventory(products, active_modules=active_modules)

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
    if CentralRegistry().getConfig("EMERGENCY_MODE"):
        if qty > 2:
            print(Colors.WARNING + " ! EMERGENCY MODE: Purchase limit is 2 units per transaction." + Colors.RESET)
            pauseScreen()
            return

    if qty > item.getAvailableStock():
        print(Colors.ERROR + " ! Not enough stock available." + Colors.RESET)
        pauseScreen()
        return

    method = paymentChoice(CentralRegistry())
    clearScreen()
    
    success = interface.purchaseItem(item, qty, method)
    showProgress(f"Processing {method} Authorization")
    
    if success:
        print(Colors.SUCCESS + f"\n [SUCCESS] {qty}x {name.title()} dispensed." + Colors.RESET)
    else:
        print(Colors.ERROR + f"\n [FAILURE] Transaction could not be completed." + Colors.RESET)
        
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

    method = paymentChoice(CentralRegistry())
    
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
    from registry.centralRegistry import CentralRegistry
    clearScreen()
    print(Colors.BOLD + " --- RESTOCK MANAGEMENT --- " + Colors.RESET)
    active_modules = CentralRegistry().getConfig("ACTIVE_MODULES") or []
    mapping = displayInventory(products, active_modules=active_modules)

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
    
    # Alerts removed as per request to keep diagnostics clean
    pauseScreen()

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
            return "EXIT"
        


def shutdownScreen(core):
    """ Cinematic minimal shutdown experience """
    width = 80
    clearScreen()
    printLogo()
    
    decommission_steps = [
        "Syncing Logs",
        "Closing Sockets",
        "Clearing Cache",
        "Detaching Hardware",
        "Core Purge"
    ]
    
    # Show a unified progress for all decommissioning tasks
    for step in decommission_steps:
        showProgress(f"DECOMMISSIONING: {step}", duration=0.4)
    
    clearScreen()
    printLogo()
    
    drawBox("SYSTEM OFFLINE", [
        "Aura Retail OS has safely powered down.",
        "",
        "  [STATUS]  Memory Purged",
        "  [STATUS]  Hardware Disconnected",
        "  [STATUS]  Session Synchronized"
    ])
    
    print("\n" + centerLine(f"{Colors.DIM}Thank you for choosing Aura Retail Technologies.{Colors.RESET}", width))
    time.sleep(1.2)

def runKiosk():
    while True:
        # --- UNIFIED BOOT SEQUENCE ---
        registry = inventory_real = monitor = payment = None
        width = 80
        
        # Splash Screen (Title Page)
        clearScreen()
        printLogo()
        print(centerLine(f"{Colors.BOLD}RETAIL OPERATING SYSTEM{Colors.RESET}", width))
        print(centerLine(f"{Colors.DIM}v4.2.0-STABLE | BUILD 2024.04{Colors.RESET}", width))
        print()
        print(centerLine(f"{Colors.CYAN}Welcome to the future of automated retail.{Colors.RESET}", width))
        print("\n" + centerLine(f"{Colors.BOLD}PRESS ENTER TO INITIALIZE AURA{Colors.RESET}", width))
        input()
        
        # --- KIOSK CONFIGURATION & PRESET SELECTION ---
        config = PersistentLayer.loadConfig()
        force_selection = config.get("ALWAYS_ASK_CONFIG", False)
        preset = config.get("KIOSK_PRESET")
        
        if not preset or force_selection:
            clearScreen()
            printLogo()
            drawBox("SYSTEM CONFIGURATION", [
                "Please select the Kiosk Application Type:",
                " [1]  Food & Beverage (Spiral Dispenser)",
                " [2]  Medical Pharmacy (Robotic Arm)",
                " [3]  Cyber-Tech Gear (Conveyor Belt)"
            ])
            
            f_choice = input(f"\n {Colors.CYAN}Application Selection >> {Colors.RESET}").strip()
            modes = {"1": "food", "2": "pharmacy", "3": "tech"}
            preset = modes.get(f_choice, "food")
            
            # Save choice for persistence
            config["KIOSK_PRESET"] = preset
            PersistentLayer.saveConfig(config)
        
        # Initialize appropriate Factory based on Preset
        if preset == "pharmacy":
            factory = PharmacyKioskFactory()
        elif preset == "tech":
            factory = TechGearFactory()
        else:
            factory = FoodKioskFactory()
            
        kiosk_type_label = factory.getKioskType()
        
        # Map kiosk type to specific inventory file
        inv_map = {
            "Aura Food & Beverage Kiosk": "inventoryFood.json",
            "Aura Medical Pharmacy Kiosk": "inventoryPharmacy.json",
            "Aura Cyber-Tech Hub": "inventoryTech.json"
        }
        inventory_file = inv_map.get(kiosk_type_label, "inventoryDefault.json")
        
        # Step 3-7: Unified Abstracted Bootstrap (Seamless transition)
        from core.bootstrapper import SystemBootstrapper
        
        # Step 3-7: Unified Abstracted Bootstrap
        interface, core, inventory_real, monitor, registry, payment = SystemBootstrapper.bootstrap(
            factory, 
            inventory_real, 
            registry, 
            payment, 
            monitor, 
            showProgress
        )
        
        inventory_items = inventory_real._items 

        print(f"\n {Colors.SUCCESS}███ AURA OS ONLINE ███{Colors.RESET}")
        time.sleep(1)

        while True:
            clearScreen()
            renderHeader(registry)

            if registry.getConfig("EMERGENCY_MODE"):
                print(centerLine(f"{Colors.ERROR}{Colors.BOLD}🚨 EMERGENCY MODE ACTIVE 🚨{Colors.RESET}", 80))
                print(centerLine(f"{Colors.WARNING}System-wide purchase limit: {Colors.BOLD}MAX 2 UNITS{Colors.RESET}{Colors.WARNING} per transaction.{Colors.RESET}", 80))
                print()
            
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
                        res = adminFlow(
                            inventory_real, 
                            registry, 
                            interface, 
                            save_callback=lambda: PersistentLayer.saveInventory(inventory_items, inventory_file)
                        )
                        if res == "REBOOT":
                            print(f" {Colors.WARNING} [SYS] Configuration change detected. Re-initializing...{Colors.RESET}")
                            time.sleep(1)
                            break # Break inner loop to re-run boot sequence
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
                shutdownScreen(core)
                return # Exit the entire runKiosk function
            else:
                print(f" {Colors.ERROR}! Invalid option. Please use 1-5.{Colors.RESET}")
                time.sleep(1)

runKiosk()
