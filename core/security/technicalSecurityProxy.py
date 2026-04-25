from utils.colors import Colors
import time

class TechnicalSecurityProxy:
    """
    PROXY PATTERN - Access Control
    Protects the technical hardware simulation menu.
    Only authorized personnel with valid Tech ID and Passkey can enter.
    """
    
    # Authorized Personnel Database
    AUTHORIZED_TECH = {
        "TECH-2024": "MASTER-HW-99",
        "ADMIN-SYS": "ROOT-ACCESS"
    }

    def __init__(self, target_menu_func):
        self._target = target_menu_func

    def authenticate_and_run(self, core):
        """ Handles the security check before delegating to the actual menu """
        print("\n" + Colors.DIM + " ══════════════════════════════════════════════════════════" + Colors.RESET)
        print(f" {Colors.WARNING}{Colors.BOLD}SECURE ACCESS REQUIRED: TECHNICAL PERSONNEL ONLY{Colors.RESET}")
        print(f" {Colors.DIM}Unauthorized access attempts are logged and monitored.{Colors.RESET}")
        
        tech_id = input(f"\n {Colors.CYAN} PERSONNEL ID  >> {Colors.RESET}").strip().upper()
        passkey = input(f" {Colors.CYAN} SECURE KEY    >> {Colors.RESET}").strip()
        
        if tech_id in self.AUTHORIZED_TECH and self.AUTHORIZED_TECH[tech_id] == passkey:
            print(f"\n {Colors.SUCCESS} ACCESS GRANTED. Welcome, {tech_id}.{Colors.RESET}")
            time.sleep(1)
            # Delegate to the real menu
            self._target(core)
        else:
            print(f"\n {Colors.ERROR} ACCESS DENIED. Invalid Credentials.{Colors.RESET}")
            from monitoring.monitoring_system import MonitoringSystem
            MonitoringSystem.notify("SECURITY", "UNAUTHORIZED_TECH_ATTEMPT", f"ID: {tech_id}")
            time.sleep(2)
