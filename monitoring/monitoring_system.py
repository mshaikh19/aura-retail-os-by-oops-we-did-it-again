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
        from utils.ui_utils import pad_ansi
        width = 75
        
        # Column width definitions
        W_TIME = 10
        W_SRC  = 12
        W_TYPE = 16
        W_MSG  = width - (W_TIME + W_SRC + W_TYPE + 13) # 13 accounts for all borders and separators: "║ " " │ " " │ " " │ " " ║"
        
        print("\n" + Colors.BLUE + " ╔" + "═"*(width-2) + "╗" + Colors.RESET)
        title_text = pad_ansi(Colors.BOLD + Colors.CYAN + "📊 SYSTEM EVENT AUDIT LOG" + Colors.RESET, width-2, 'center')
        print(f" {Colors.BLUE}║{title_text}{Colors.BLUE}║{Colors.RESET}")
        print(Colors.BLUE + " ╠" + "═"*(width-2) + "╣" + Colors.RESET)
        
        if not cls._alerts:
            empty_msg = pad_ansi(Colors.DIM + "No critical security or hardware events recorded." + Colors.RESET, width-2, 'center')
            print(f" {Colors.BLUE}║{empty_msg}{Colors.BLUE}║{Colors.RESET}")
        else:
            # Header Row
            h_time = pad_ansi(f"{Colors.BOLD}TIME", W_TIME, 'center')
            h_src  = pad_ansi(f"{Colors.BOLD}SOURCE", W_SRC, 'center')
            h_type = pad_ansi(f"{Colors.BOLD}EVENT", W_TYPE, 'center')
            h_msg  = pad_ansi(f"{Colors.BOLD}AUDIT DETAIL", W_MSG, 'center')
            print(f" {Colors.BLUE}║ {h_time} │ {h_src} │ {h_type} │ {h_msg} ║{Colors.RESET}")
            
            # Separator
            print(Colors.BLUE + " ╟" + "─"*(W_TIME+1) + "┼" + "─"*(W_SRC+2) + "┼" + "─"*(W_TYPE+2) + "┼" + "─"*(W_MSG+1) + "╢" + Colors.RESET)

            for alert in cls._alerts:
                # Color logic
                src_color = Colors.CYAN if alert["src"] == "BOOT_SCAN" else Colors.HEADER
                type_color = Colors.ERROR if "FAIL" in alert["type"] or "LOW" in alert["type"] else Colors.SUCCESS
                if alert["type"] == "MODULE_ATTACHED": type_color = Colors.HEADER
                if alert["type"] == "SYSTEM_READY": type_color = Colors.CYAN

                c_time = pad_ansi(f"{Colors.DIM}{alert['time']}{Colors.RESET}", W_TIME, 'center')
                c_src  = pad_ansi(f"{src_color}{alert['src']:^10}{Colors.RESET}", W_SRC, 'center')
                c_type = pad_ansi(f"{type_color}{alert['type']:^14}{Colors.RESET}", W_TYPE, 'center')
                c_msg  = pad_ansi(f" {Colors.TEXT}{alert['msg']}{Colors.RESET}", W_MSG, 'left')
                
                print(f" {Colors.BLUE}║ {c_time} │ {c_src} │ {c_type} │ {c_msg} ║{Colors.RESET}")
        
        print(Colors.BLUE + " ╚" + "═"*(width-2) + "╝" + Colors.RESET + "\n")
