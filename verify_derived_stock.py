import sys
import io
import os

# Force UTF-8 encoding for premium UI rendering on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from models.productModel import ProductModel

from inventory.components.simpleProduct import SimpleProduct
from hardware.interfaces.hardwareAbstraction import HardwareAbstraction
from hardware.dispensers.spiralDispenser import SpiralDispenser
from registry.central_registry import CentralRegistry
from utils.colors import Colors

def verify_derived_stock():
    print(f"{Colors.HEADER}=== VERIFYING DERIVED STOCK (REQUIREMENT 4.1) ==={Colors.RESET}")
    
    # 1. Setup Registry and Hardware
    registry = CentralRegistry()
    dispenser = SpiralDispenser()
    hardware = HardwareAbstraction(dispenser)
    registry.registerHardware(hardware)
    
    # 2. Setup Product
    model = ProductModel("P001", "Chips", 20.0, stock=10)
    product = SimpleProduct(model)
    
    print(f"\n[STEP 1] Initial State")
    print(f"Product: {product.getName()}, Physical Stock: {product.getStock()}, Available: {product.getAvailableStock()}")
    
    if product.getAvailableStock() != 10:
        print(f"{Colors.ERROR}FAIL: Initial available stock should be 10{Colors.RESET}")
        return False
    
    # 3. Simulate Jam
    print(f"\n[STEP 2] Simulating Jam for 'Chips'")
    hardware.toggleProductJam("Chips")
    
    print(f"Jammed: {hardware.isProductJammed('Chips')}")
    print(f"Physical Stock: {product.getStock()}, Available Stock: {product.getAvailableStock()}")
    
    if product.getAvailableStock() != 0:
        print(f"{Colors.ERROR}FAIL: Available stock should be 0 when jammed{Colors.RESET}")
        return False
    
    print(f"{Colors.SUCCESS}PASS: Available stock reported as 0 despite physical stock exists.{Colors.RESET}")
    
    # 4. Unjam
    print(f"\n[STEP 3] Simulating Unjam for 'Chips'")
    hardware.toggleProductJam("Chips")
    
    print(f"Jammed: {hardware.isProductJammed('Chips')}")
    print(f"Physical Stock: {product.getStock()}, Available Stock: {product.getAvailableStock()}")
    
    if product.getAvailableStock() != 10:
        print(f"{Colors.ERROR}FAIL: Available stock should return to physical stock when unjammed{Colors.RESET}")
        return False
    
    print(f"{Colors.SUCCESS}PASS: Available stock restored to physical stock.{Colors.RESET}")
    
    print(f"\n{Colors.SUCCESS}VERIFICATION COMPLETE: Derived Available Stock is working correctly!{Colors.RESET}")
    return True

if __name__ == "__main__":
    import sys
    import os
    # Add project root to path
    sys.path.append(os.getcwd())
    verify_derived_stock()
