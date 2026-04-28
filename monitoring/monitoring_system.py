import datetime
from utils.colors import Colors

class MonitoringSystem:
    def __init__(self):
        print(f" {Colors.SUCCESS}◈ {Colors.BOLD}MONITORING:{Colors.RESET} {Colors.TEXT}Sentinel system active.{Colors.RESET}")
    """
    observer Pattern
    The MonitoringSystem acts as the Subject/Publisher.
    It tracks failures, alerts, and system events. Subsystems can fire events here,
    and other parts of the system can subscribe to listen to them without being tightly coupled.
    """
    
    _subscribers = {}
    _alerts = []

    @classmethod
    def subscribe(cls, event_type, handler):
        if event_type not in cls._subscribers:
            cls._subscribers[event_type] = []
        cls._subscribers[event_type].append(handler)
        print(f"{Colors.SUCCESS}[MONITORING]{Colors.RESET} Subscriber added for event: {event_type}")

    @classmethod
    def notify(cls, source, event_type, detail=""):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        cls._alerts.append({
            "time": timestamp,
            "src": source,
            "type": event_type,
            "msg": detail
        })
        # Internal log redirected to memory only, no console output

        if event_type in cls._subscribers:
            for handler in cls._subscribers[event_type]:
                try:
                    handler(source, detail)
                except Exception as e:
                    pass

    @classmethod
    def getAlerts(cls):
        return cls._alerts

    @classmethod
    def showAlerts(cls):
        from utils.ui_utils import pad_ansi, strip_ansi
        width = 100 # Increased for better visibility
        
        # Column width definitions
        W_TIME = 10
        W_SRC  = 12
        W_TYPE = 16
        # Calculation: indent(1) + ║(1) + space(1) + T + space(1) + │(1) + space(1) + S + space(1) + │(1) + space(1) + E + space(1) + │(1) + space(1) + M + space(1) + ║(1)
        # Total fixed = 1+1+1 + 1+1+1 + 1+1+1 + 1+1+1 + 1+1 = 16 (including spaces around content)
        W_MSG  = width - (W_TIME + W_SRC + W_TYPE + 13) 
        
        indent = " "
        print("\n" + indent + Colors.BLUE + "╔" + "═"*(width-2) + "╗" + Colors.RESET)
        title_text = pad_ansi(Colors.BOLD + Colors.CYAN + "📊 SYSTEM EVENT AUDIT LOG" + Colors.RESET, width-4, 'center')
        print(f"{indent}{Colors.BLUE}║ {title_text} ║{Colors.RESET}")
        print(indent + Colors.BLUE + "╠" + "═"*(width-2) + "╣" + Colors.RESET)
        
        if not cls._alerts:
            empty_msg = pad_ansi(Colors.DIM + "No critical security or hardware events recorded." + Colors.RESET, width-4, 'center')
            print(f"{indent}{Colors.BLUE}║ {empty_msg} ║{Colors.RESET}")
        else:
            # Header Row
            h_time = pad_ansi(f"{Colors.BOLD}TIME", W_TIME, 'center')
            h_src  = pad_ansi(f"{Colors.BOLD}SOURCE", W_SRC, 'center')
            h_type = pad_ansi(f"{Colors.BOLD}EVENT", W_TYPE, 'center')
            h_msg  = pad_ansi(f"{Colors.BOLD}AUDIT DETAIL", W_MSG, 'center')
            print(f"{indent}{Colors.BLUE}║ {h_time} │ {h_src} │ {h_type} │ {h_msg} ║{Colors.RESET}")
            
            # Separator: ╟───┼───┼───┼───╢
            sep = f"{indent}{Colors.BLUE}╟{'─'*(W_TIME+2)}┼{'─'*(W_SRC+2)}┼{'─'*(W_TYPE+2)}┼{'─'*(W_MSG+2)}╢{Colors.RESET}"
            print(sep)

            for alert in cls._alerts:
                # Color logic
                src_color = Colors.CYAN if alert["src"] == "BOOT_SCAN" else Colors.HEADER
                type_color = Colors.ERROR if "FAIL" in alert["type"] or "LOW" in alert["type"] else Colors.SUCCESS
                if alert["type"] == "MODULE_ATTACHED": type_color = Colors.HEADER
                if alert["type"] == "SYSTEM_READY": type_color = Colors.CYAN

                msg = alert["msg"]
                if len(msg) > W_MSG:
                    msg = msg[:W_MSG-3] + "..."

                c_time = pad_ansi(f"{Colors.DIM}{alert['time']}{Colors.RESET}", W_TIME, 'center')
                c_src  = pad_ansi(f"{src_color}{alert['src']}{Colors.RESET}", W_SRC, 'center')
                c_type = pad_ansi(f"{type_color}{alert['type']}{Colors.RESET}", W_TYPE, 'center')
                c_msg  = pad_ansi(f"{Colors.TEXT}{msg}{Colors.RESET}", W_MSG, 'left')
                
                print(f"{indent}{Colors.BLUE}║ {c_time} │ {c_src} │ {c_type} │ {c_msg} ║{Colors.RESET}")
        
        print(indent + Colors.BLUE + "╚" + "═"*(width-2) + "╝" + Colors.RESET + "\n")
