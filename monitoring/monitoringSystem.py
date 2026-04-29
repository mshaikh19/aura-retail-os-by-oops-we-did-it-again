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
        from utils.ui_utils import render_table
        
        if not cls._alerts:
            from utils.ui_utils import drawBox
            drawBox("SYSTEM EVENT AUDIT LOG", ["No critical security or hardware events recorded."])
            return

        headers = ["TIME", "SOURCE", "EVENT", "AUDIT DETAIL"]
        rows = []

        for alert in cls._alerts:
            # Color logic
            src_color = Colors.CYAN if alert["src"] == "BOOT_SCAN" else Colors.HEADER
            type_color = Colors.ERROR if "FAIL" in alert["type"] or "LOW" in alert["type"] else Colors.SUCCESS
            if alert["type"] == "MODULE_ATTACHED": type_color = Colors.HEADER
            if alert["type"] == "SYSTEM_READY": type_color = Colors.CYAN

            msg = alert["msg"]
            # Truncate to ensure the table fits within 80 chars
            # (Time: 8, Source: 12, Event: 16, Padding: 8, Separators: 3, Borders: 2 = 49 fixed)
            # 80 - 49 = 31 available for message
            if len(msg) > 31:
                msg = msg[:28] + "..."

            rows.append([
                f"{Colors.DIM}{alert['time']}{Colors.RESET}",
                f"{src_color}{alert['src']}{Colors.RESET}",
                f"{type_color}{alert['type']}{Colors.RESET}",
                f"{Colors.TEXT}{msg}{Colors.RESET}"
            ])
        
        render_table(headers, rows, title="SYSTEM EVENT AUDIT LOG", alignments=["center", "center", "center", "left"])
