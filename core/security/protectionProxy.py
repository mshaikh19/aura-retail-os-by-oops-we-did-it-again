from utils.colors import Colors
import time

class TechnicianSecurityProxy:
    """
    PROTECTION PROXY PATTERN
    Intercepts calls to sensitive hardware simulation functions.
    Ensures only authorized technicians with a valid ID can modify the stack.
    """
    
    def __init__(self, core_system):
        self._core = core_system
        self._authorized = False

    def authenticate(self, tech_id):
        """ Validates the technician ID """
        # In a real system, this would check a secure database
        valid_ids = ["TECH-777", "ADMIN-001"]
        
        if tech_id in valid_ids:
            self._authorized = True
            print(f" {Colors.SUCCESS}[AUTH] Access Granted: {tech_id}{Colors.RESET}")
            time.sleep(0.8)
            return True
        else:
            print(f" {Colors.ERROR}[AUTH] Invalid Technician ID. Logging attempt...{Colors.RESET}")
            time.sleep(1.2)
            return False

    def attachModule(self, module):
        if self._authorized:
            self._core.attachModule(module)
        else:
            print(f" {Colors.ERROR}[SECURITY] Unauthorized attempt to modify hardware!{Colors.RESET}")

    def swapDispenser(self, new_dispenser):
        if self._authorized:
            self._core.hardwareSystem.swapDispenser(new_dispenser)
        else:
            print(f" {Colors.ERROR}[SECURITY] Unauthorized hardware swap attempt!{Colors.RESET}")

    def clearExtensions(self):
        if self._authorized:
            self._core.top_module = None
            print(f" {Colors.WARNING}[CORE] All hardware extensions cleared.{Colors.RESET}")
        else:
            print(f" {Colors.ERROR}[SECURITY] Unauthorized clear request!{Colors.RESET}")

    def getModuleStatuses(self):
        # Read operations are generally allowed even if not authorized
        return self._core.getModuleStatuses()
