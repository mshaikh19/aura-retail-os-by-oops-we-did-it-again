import time
from inventory.components.simpleProduct import SimpleProduct
from inventory.components.productBundle import ProductBundle
from persistence.persistenceLayer import PersistentLayer
from monitoring.monitoring_system import MonitoringSystem

from utils.colors import Colors
from utils.ui_utils import drawBox

def clearScreen():
    import os
    if os.name == 'nt': os.system('cls')
    else: os.system('clear')
    print("\033[H\033[2J\033[3J", end="", flush=True)

def pauseScreen():
    from utils.ui_utils import pad_ansi
    print(f"\n {Colors.DIM}─" + "─"*58 + Colors.RESET)
    input(f" >> Press ENTER to return to menu...")



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
            from utils.ui_utils import pad_ansi
            
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
                    c_time = pad_ansi(f"{Colors.DIM}{t['timestamp']}{Colors.RESET}", 20, 'left')
                    c_asset = pad_ansi(name, 12, 'left')
                    c_vol = pad_ansi(str(t['quantity']), 4, 'center')
                    c_rev = pad_ansi(f"{Colors.SUCCESS}Rs.{t['total_amount']:>9.2f}{Colors.RESET}", 12, 'right')
                    print(f" {Colors.CYAN}║{Colors.RESET} {c_time} {Colors.CYAN}║{Colors.RESET} {c_asset} {Colors.CYAN}║{Colors.RESET} {c_vol} {Colors.CYAN}║{Colors.RESET} {c_rev} {Colors.CYAN}║{Colors.RESET}")
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

            from utils.ui_utils import pad_ansi
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
                    
                    c_name = pad_ansi(item.model.name, 28, 'left')
                    c_stock = pad_ansi(str(stock), 12, 'center')
                    c_status = pad_ansi(status, 16, 'center')
                    print(f" {Colors.HEADER}║{Colors.RESET} {c_name} {Colors.HEADER}║{Colors.RESET} {c_stock} {Colors.HEADER}║{Colors.RESET} {c_status} {Colors.HEADER}║{Colors.RESET}")
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
            from utils.ui_utils import pad_ansi
            print(f"\n {Colors.HEADER} ⚙ CONFIGURATION: PRICING & DISCOUNTS{Colors.RESET}")
            print(f" {Colors.DIM}╔{'═'*60}╗{Colors.RESET}")
            keys = list(items.keys())
            for i, k in enumerate(keys, 1):
                item = items[k]
                val = f"Rs.{item.getPrice():.2f}"
                if isinstance(item, ProductBundle): 
                    val += f" ({Colors.WARNING}{item._discount*100}% Disc{Colors.RESET})"
                
                content = f" [{i}] {item.getName():<25} | {val}"
                line_text = pad_ansi(content, 58, 'left')
                print(f" {Colors.DIM}║{Colors.RESET} {line_text} {Colors.DIM}║{Colors.RESET}")
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
            # MAINTENANCE: Consolidation to Minimal Options
            while True:
                clearScreen()
                config = PersistentLayer.loadConfig()
                always_ask = config.get("ALWAYS_ASK_CONFIG", False)
                ask_status = f"{Colors.SUCCESS}ON{Colors.CYAN}" if always_ask else f"{Colors.ERROR}OFF{Colors.CYAN}"
                
                drawBox("SYSTEM CONFIGURATION & MAINTENANCE", [
                    f" [1]  Re-Configure Kiosk (Type & Boot)",
                    f" [2]  Factory Reset (Clear Logs & Status)",
                    f" [3]  Back to Administration"
                ])
                
                m_choice = input(f"\n {Colors.CYAN}Selection >> {Colors.RESET}").strip()
                if m_choice == "1":
                    # Combined Re-config
                    clearScreen()
                    drawBox("RE-CONFIGURATION NODE", [
                        f" Status: {ask_status}",
                        "",
                        " [T] Toggle 'Always Ask' on Boot",
                        " [C] Change Kiosk Type (Direct)",
                        " [B] Back"
                    ])
                    opt = input(f"\n {Colors.CYAN}Sub-Selection >> {Colors.RESET}").strip().upper()
                    if opt == "T":
                        config["ALWAYS_ASK_CONFIG"] = not always_ask
                        PersistentLayer.saveConfig(config)
                        print(f" {Colors.SUCCESS} Boot configuration updated.{Colors.RESET}")
                        time.sleep(1)
                        return "REBOOT"
                    elif opt == "C":
                        drawBox("SWITCH KIOSK MODE", [
                            " [1]  Food & Beverage",
                            " [2]  Medical Pharmacy",
                            " [3]  Cyber-Tech Gear",
                            " [4]  Cancel"
                        ])
                        nm = input(f"\n {Colors.CYAN}New Mode >> {Colors.RESET}").strip()
                        modes = {"1": "food", "2": "pharmacy", "3": "tech"}
                        if nm in modes:
                            config["KIOSK_PRESET"] = modes[nm]
                            PersistentLayer.saveConfig(config)
                            print(f" {Colors.SUCCESS} Mode changed to {modes[nm].upper()}.{Colors.RESET}")
                            time.sleep(1)
                            return "REBOOT"
                    continue
                elif m_choice == "2":
                    core.setSystemStatus("ACTIVE")
                    MonitoringSystem._alerts = []
                    print(f" {Colors.SUCCESS} System logs and status have been reset.{Colors.RESET}")
                    time.sleep(1)
                elif m_choice == "3":
                    break

        elif choice == "7":
            return "EXIT"
