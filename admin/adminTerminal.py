import time
from inventory.components.simpleProduct import SimpleProduct
from inventory.components.productBundle import ProductBundle
from persistence.persistenceLayer import PersistentLayer
from monitoring.monitoring_system import MonitoringSystem

from utils.colors import Colors

def clearScreen():
    print("\033[H\033[J", end="")

def pauseScreen():
    print(f"\n {Colors.DIM}─" + "─"*58 + Colors.RESET)
    input(f" >> Press ENTER to return to menu...")

def drawBox(title, lines):
    width = 60
    print(Colors.BLUE + "╔" + "═"*(width-2) + "╗")
    print(f"║{Colors.BOLD}{title:^58}{Colors.RESET}{Colors.BLUE}║")
    print("╠" + "═"*(width-2) + "╣")
    for line in lines:
        print(f"║ {line:<57}║")
    print("╚" + "═"*(width-2) + "╝" + Colors.RESET)

def adminFlow(inventory_real, registry, interface, save_callback):
    """ 
    ADMINISTRATIVE MODULE
    Decoupled from the main customer terminal.
    Handles Inventory Health, Sales Analytics, and Configuration.
    """
    kiosk_type = registry.getConfig("TYPE") or "CORE"

    while True:
        clearScreen()
        print(f"\n {Colors.HEADER}{Colors.BOLD} AURA OS | {kiosk_type.upper()} ADMIN{Colors.RESET}")
        print(f" {Colors.DIM}" + "-"*58 + Colors.RESET)
        items = inventory_real._items
        total_items = len([i for i in items.values() if isinstance(i, SimpleProduct)])
        low_stock = len([i for i in items.values() if isinstance(i, SimpleProduct) and i.getAvailableStock() < 5])
        
        core = registry.getKiosk("AURA-001")
        sys_status = core.getSystemStatus()
        status_color = Colors.SUCCESS if sys_status == "ACTIVE" else (Colors.WARNING if sys_status == "EMERGENCY" else Colors.ERROR)

        print(f" {Colors.CYAN}SYSTEM STATUS:{Colors.RESET} {status_color}{sys_status}{Colors.RESET} | "
              f"{Colors.CYAN}PRODUCTS:{Colors.RESET} {total_items} | "
              f"{Colors.CYAN}CRITICAL STOCK:{Colors.RESET} {Colors.ERROR if low_stock > 0 else Colors.SUCCESS}{low_stock}{Colors.RESET}")
        
        # Show formatted recent alert
        alerts = MonitoringSystem.getAlerts()
        if alerts:
            a = alerts[-1]
            alert_line = f"{Colors.DIM}[{a['time']}] {Colors.HEADER}{a['src']}: {Colors.RESET}{a['msg']}"
            print(f" {Colors.WARNING}RECENT ALERT:{Colors.RESET} {alert_line}")
        else:
            print(f" {Colors.DIM}RECENT ALERTS: NO CRITICAL EVENTS{Colors.RESET}")
        
        print(f" {Colors.DIM}─" + "─"*58 + Colors.RESET)
        
        drawBox("ADMINISTRATION SUITE", [
            " [1]  Revenue & Performance Data",
            " [2]  Inventory Health & Restock",
            " [3]  Price & Discount Configuration",
            " [4]  System Deep-Scan Audit",
            " [5]  Toggle EMERGENCY Mode",
            " [6]  Maintenance: Reset System/Preset",
            " [7]  Exit Management Shell"
        ])
        
        print(f"\n {Colors.CYAN}Command{Colors.RESET} {Colors.DIM}>>{Colors.RESET} ", end="")
        choice = input().strip()
        
        if choice == "1":
            clearScreen()
            all_transactions = PersistentLayer.load("transactions.json")
            
            # Filter by kiosk type
            transactions = [t for t in all_transactions if t.get('kiosk_type') == kiosk_type]
            
            print(f"\n {Colors.HEADER} 📋 SALES ANALYTICS: {kiosk_type.upper()}{Colors.RESET}")
            if not transactions:
                print(f"\n {Colors.DIM}  No transaction data found for this kiosk type.{Colors.RESET}")
            else:
                # Premium Double-Line Table
                top = f"╔{'═'*22}╦{'═'*14}╦{'═'*6}╦{'═'*14}╗"
                sep = f"╠{'═'*22}╬{'═'*14}╬{'═'*6}╬{'═'*14}╣"
                bot = f"╚{'═'*22}╩{'═'*14}╩{'═'*6}╩{'═'*14}╝"
                header = f"║ {'DATA TIMESTAMP':^20} ║ {'ASSET ID':^12} ║ {'VOL':^4} ║ {'REVENUE':^12} ║"

                print(f" {Colors.CYAN}{top}{Colors.RESET}")
                print(f" {Colors.CYAN}{header}{Colors.RESET}")
                print(f" {Colors.CYAN}{sep}{Colors.RESET}")
                
                for t in transactions[-12:]:
                    name = t['product_name'][:12]
                    print(f" {Colors.CYAN}║{Colors.RESET} {Colors.DIM}{t['timestamp']:<20}{Colors.RESET} {Colors.CYAN}║{Colors.RESET} {name:<12} {Colors.CYAN}║{Colors.RESET} {t['quantity']:^4} {Colors.CYAN}║{Colors.RESET} {Colors.SUCCESS}Rs.{t['total_amount']:>9.2f}{Colors.RESET} {Colors.CYAN}║{Colors.RESET}")
                print(f" {Colors.CYAN}{bot}{Colors.RESET}")
                
                total = sum(t['total_amount'] for t in transactions)
                print(f"\n {Colors.HEADER} REVENUE TOTAL: {Colors.SUCCESS}Rs.{total:.2f}{Colors.RESET}")
            pauseScreen()
            
        elif choice == "2":
            clearScreen()
            print(f"\n {Colors.HEADER} 📦 INVENTORY HEALTH MONITOR{Colors.RESET}")
            # Premium Health Table
            top = f"╔{'═'*30}╦{'═'*14}╦{'═'*18}╗"
            sep = f"╠{'═'*30}╬{'═'*14}╬{'═'*18}╣"
            bot = f"╚{'═'*30}╩{'═'*14}╩{'═'*18}╝"
            header = f"║ {'ASSET NAME':<28} ║ {'UNIT COUNT':^12} ║ {'HEALTH STATUS':^16} ║"

            print(f" {Colors.HEADER}{top}{Colors.RESET}")
            print(f" {Colors.HEADER}{header}{Colors.RESET}")
            print(f" {Colors.HEADER}{sep}{Colors.RESET}")
            
            product_keys = []
            for name, item in items.items():
                if isinstance(item, SimpleProduct):
                    product_keys.append(name)
                    stock = item.getAvailableStock()
                    status = f"{Colors.SUCCESS}STABLE{Colors.RESET}"
                    if stock < 5: status = f"{Colors.ERROR}CRITICAL{Colors.RESET}"
                    elif stock < 10: status = f"{Colors.WARNING}WARNING{Colors.RESET}"
                    
                    print(f" {Colors.HEADER}║{Colors.RESET} {item.model.name:<28} {Colors.HEADER}║{Colors.RESET} {stock:^12} {Colors.HEADER}║{Colors.RESET} {status:^16} {Colors.HEADER}║{Colors.RESET}")
            print(f" {Colors.HEADER}{bot}{Colors.RESET}")
            
            print(f"\n [R] Restock Specific Item | [B] Bulk Restock (50) | [X] Back")
            sub = input(f" {Colors.CYAN}Selection >> {Colors.RESET}").strip().upper()
            
            if sub == "R":
                ref = input(" Enter Name or Index: ").strip()
                try:
                    target = product_keys[int(ref)-1] if ref.isdigit() else ref.lower()
                    qty = int(input(f" Quantity to add to {target}: "))
                    interface.restockInventory(items[target], qty)
                except: print(f" {Colors.ERROR}Operation Failed.{Colors.RESET}")
            elif sub == "B":
                for name, item in items.items():
                    if hasattr(item, 'model'): item.model.stock = 50
                save_callback()
                print(f" {Colors.SUCCESS}Bulk restock complete.{Colors.RESET}")
                time.sleep(1)
                
        elif choice == "3":
            clearScreen()
            print(f"\n {Colors.HEADER} ⚙ CONFIGURATION: PRICING & DISCOUNTS{Colors.RESET}")
            print(f" {Colors.DIM}╔{'═'*60}╗{Colors.RESET}")
            keys = list(items.keys())
            for i, k in enumerate(keys, 1):
                item = items[k]
                val = f"Rs.{item.getPrice():.2f}"
                if isinstance(item, ProductBundle): 
                    val += f" ({Colors.WARNING}{item._discount*100}% Disc{Colors.RESET})"
                
                line = f" [{i}] {item.getName():<25} | {val}"
                print(f" {Colors.DIM}║{Colors.RESET} {line:<58} {Colors.DIM}║{Colors.RESET}")
            print(f" {Colors.DIM}╚{'═'*60}╝{Colors.RESET}")
            
            idx = input(f"\n {Colors.CYAN}Select Index to configure:{Colors.RESET} ").strip()
            try:
                target_name = keys[int(idx)-1]
                target_item = items[target_name]
                if isinstance(target_item, SimpleProduct):
                    target_item.model.price = float(input(f" New Price for {target_name}: "))
                else:
                    target_item._discount = float(input(f" New Discount (0.0-1.0) for {target_name}: "))
                save_callback()
                print(f" {Colors.SUCCESS} Configuration updated.{Colors.RESET}")
                time.sleep(1)
            except: pass

        elif choice == "4":
            clearScreen()
            interface.runDiagnostics()
            pauseScreen()
            
        elif choice == "5":
            if core.getSystemStatus() == "EMERGENCY":
                core.setSystemStatus("ACTIVE")
                registry.setConfig("EMERGENCY_MODE", False)
                PersistentLayer.saveConfig(registry._config)
                print(f" {Colors.SUCCESS} Emergency Mode DEACTIVATED.{Colors.RESET}")
            else:
                core.setSystemStatus("EMERGENCY")
                registry.setConfig("EMERGENCY_MODE", True)
                PersistentLayer.saveConfig(registry._config)
                print(f" {Colors.WARNING} Emergency Mode ACTIVATED.{Colors.RESET}")
            time.sleep(1.5)

        elif choice == "6":
            clearScreen()
            drawBox("MAINTENANCE OPERATIONS", [
                " [1]  Reset System Status to ACTIVE (Clear Errors)",
                " [2]  Wipe Kiosk Preset (Force Re-select on Boot)",
                " [3]  Back"
            ])
            m_choice = input(f"\n {Colors.CYAN}Selection >> {Colors.RESET}").strip()
            if m_choice == "1":
                core.setSystemStatus("ACTIVE")
                print(f" {Colors.SUCCESS} System status reset to ACTIVE.{Colors.RESET}")
            elif m_choice == "2":
                config = PersistentLayer.loadConfig()
                if "KIOSK_PRESET" in config:
                    del config["KIOSK_PRESET"]
                    PersistentLayer.saveConfig(config)
                    print(f" {Colors.SUCCESS} Preset wiped. Restart app to reconfigure.{Colors.RESET}")
                else:
                    print(f" {Colors.DIM} No preset found to wipe.{Colors.RESET}")
            time.sleep(1.5)

        elif choice == "7":
            break