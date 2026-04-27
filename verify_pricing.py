import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from models.productModel import ProductModel
from inventory.components.simpleProduct import SimpleProduct
from inventory.components.productBundle import ProductBundle
from registry.central_registry import CentralRegistry
from inventory.pricing.pricing_policy import StandardPricingPolicy, DiscountedPricingPolicy, EmergencyPricingPolicy

def test_pricing():
    print("--- Testing Dynamic Pricing System ---")
    
    # 1. Setup products
    p1_model = ProductModel("P001", "Laptop", 1000.0, 10)
    p2_model = ProductModel("P002", "Mouse", 50.0, 50)
    
    product1 = SimpleProduct(p1_model)
    product2 = SimpleProduct(p2_model)
    
    bundle = ProductBundle("Tech Bundle", discount=0.05) # 5% bundle discount
    bundle.add(product1)
    bundle.add(product2)
    
    registry = CentralRegistry()
    
    # 2. Verify Standard Pricing
    print("\n[SCENARIO] Standard Pricing")
    registry.setPricingPolicy(StandardPricingPolicy())
    print(f"Product 1 Price: {product1.getPrice()} (Expected: 1000.0)")
    print(f"Product 2 Price: {product2.getPrice()} (Expected: 50.0)")
    print(f"Bundle Price: {bundle.getPrice()} (Expected: (1000+50)*0.95 = 997.5)")
    
    assert product1.getPrice() == 1000.0
    assert product2.getPrice() == 50.0
    assert abs(bundle.getPrice() - 997.5) < 0.001
    
    # 3. Verify Discounted Pricing (10% off)
    print("\n[SCENARIO] Discounted Pricing (10% off)")
    registry.setPricingPolicy(DiscountedPricingPolicy(0.1))
    print(f"Product 1 Price: {product1.getPrice()} (Expected: 900.0)")
    print(f"Product 2 Price: {product2.getPrice()} (Expected: 45.0)")
    print(f"Bundle Price: {bundle.getPrice()} (Expected: (900+45)*0.95 = 897.75)")
    
    assert product1.getPrice() == 900.0
    assert product2.getPrice() == 45.0
    assert abs(bundle.getPrice() - 897.75) < 0.001
    
    # 4. Verify Emergency Pricing (20% markup)
    print("\n[SCENARIO] Emergency Pricing (20% markup)")
    registry.setPricingPolicy(EmergencyPricingPolicy(0.2))
    print(f"Product 1 Price: {product1.getPrice()} (Expected: 1200.0)")
    print(f"Product 2 Price: {product2.getPrice()} (Expected: 60.0)")
    print(f"Bundle Price: {bundle.getPrice()} (Expected: (1200+60)*0.95 = 1197.0)")
    
    assert product1.getPrice() == 1200.0
    assert product2.getPrice() == 60.0
    assert abs(bundle.getPrice() - 1197.0) < 0.001
    
    print("\n--- All Pricing Tests Passed! ---")

if __name__ == "__main__":
    test_pricing()
