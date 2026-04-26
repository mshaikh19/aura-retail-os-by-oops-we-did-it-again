from utils.colors import Colors
import datetime

class MonitoringSystem:
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
        print(f"{Colors.CYAN}[MONITORING]{Colors.RESET} Subscriber added for: {Colors.BOLD}{event_type}{Colors.RESET}")

    @classmethod
    def notify(cls, source, event_type, detail=""):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alert_msg = f"{Colors.DIM}[{timestamp}]{Colors.RESET} {Colors.HEADER}[{source}]{Colors.RESET} {Colors.BOLD}{event_type}{Colors.RESET}: {detail}"
        
        cls._alerts.append(alert_msg)
        print(f"{Colors.CYAN}[MONITORING]{Colors.RESET} {alert_msg}")

        # Notify all subscribers listening to this specific event
        if event_type in cls._subscribers:
            for handler in cls._subscribers[event_type]:
                try:
                    handler(source, detail)
                except Exception as e:
                    print(f"[MONITORING ERROR] Handler failed for {event_type}: {str(e)}")

    @classmethod
    def getAlerts(cls):
        return cls._alerts

    @classmethod
    def showAlerts(cls):
        print("\n=== SYSTEM ALERTS & LOGS ===")
        if not cls._alerts:
            print("No alerts recorded.")
        else:
            for alert in cls._alerts:
                print(alert)
        print("============================\n")
