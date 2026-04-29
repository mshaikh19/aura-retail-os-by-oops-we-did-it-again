"""Structured simulation demo for Aura Retail OS Path B features.

Run:
    python demo/simulate_system.py

Demonstrates:
1) Successful purchase
2) Hardware failure -> atomic rollback
3) Runtime hot-swap waiting for in-flight command
"""

import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.commands.purchaseCommand import PurchaseCommand
from core.kioskCoreSystem import KioskCoreSystem
from core.sessionManager import SessionManager
from hardware.dispensers.roboticDispenser import RoboticDispenser
from hardware.dispensers.spiralDispenser import SpiralDispenser
from hardware.interfaces.hardwareAbstraction import HardwareAbstraction
from inventory.components.inventoryManager import InventorySystem
from inventory.components.productBundle import ProductBundle
from inventory.components.simpleProduct import SimpleProduct
from models.productModel import ProductModel
from models.transaction import Transaction


class SimulatedPaymentSystem:
    """In-memory payment system for deterministic demo output."""

    def __init__(self):
        self.transaction_history = []
        self.refund_count = 0

    def makePayment(self, method, amount, product_name=None, quantity=None, kiosk_type="UNKNOWN"):
        tx = Transaction(
            product_name=product_name or "UNKNOWN",
            quantity=quantity or 0,
            total_amount=amount,
            payment_method=method,
            status="SUCCESS",
            kiosk_type=kiosk_type,
            payment_details={"simulated": True},
        )
        self.transaction_history.append(tx)
        return tx

    def refund(self, method):
        self.refund_count += 1
        if self.transaction_history:
            self.transaction_history[-1].status = "REFUNDED"
        return True

    def getTransactionHistory(self):
        return self.transaction_history


class LongRunningCommand:
    """Simple command to simulate an in-flight operation during hot-swap."""

    def __init__(self, duration_s=1.5):
        self.duration_s = duration_s

    def execute(self, core):
        time.sleep(self.duration_s)
        return True


def section(title):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def step(number, title, details=None):
    print(f"\nSTEP {number}: {title}")
    if details:
        for line in details:
            print(f"  - {line}")


def checkpoint(name, condition, details=""):
    label = "PASS" if condition else "FAIL"
    suffix = f" | {details}" if details else ""
    print(f"[{label}] {name}{suffix}")


def stock_of(inv, key):
    item = inv.getProduct(key)
    if item and hasattr(item, "model"):
        return item.model.stock
    return None


def state_snapshot(core, payment, inventory, label):
    print(f"\n[STATE SNAPSHOT] {label}")
    print(f"  system_status      = {core.getSystemStatus()}")
    print(f"  active_dispenser   = {core.hardwareSystem.getStatus().get('dispenser')}")
    print(f"  cable_stock        = {stock_of(inventory, 'cable')}")
    print(f"  tx_count           = {len(payment.getTransactionHistory())}")
    print(f"  refund_count       = {payment.refund_count}")


def print_new_transaction(payment, before_count):
    after_count = len(payment.getTransactionHistory())
    if after_count > before_count:
        tx = payment.getTransactionHistory()[-1]
        print("  New transaction:")
        print(f"    id      : {tx.transaction_id}")
        print(f"    product : {tx.product_name}")
        print(f"    qty     : {tx.quantity}")
        print(f"    amount  : {tx.total_amount}")
        print(f"    method  : {tx.payment_method}")
        print(f"    status  : {tx.status}")


def build_inventory():
    inv = InventorySystem()

    p_powerbank = SimpleProduct(ProductModel("p-pb", "PowerBank 20k", 1200, 5))
    p_cable = SimpleProduct(ProductModel("p-cbl", "USB-C Cable", 300, 10))

    bundle = ProductBundle("Creator Kit", discount=0.05)
    bundle.add(p_powerbank)
    bundle.add(p_cable)

    inv.addProduct("powerbank", p_powerbank)
    inv.addProduct("cable", p_cable)
    inv.addProduct("creator_kit", bundle)
    return inv, p_cable


def print_summary(core, payment, inventory):
    section("Simulation Summary")
    print(f"System status        : {core.getSystemStatus()}")
    print(f"Active dispenser     : {core.hardwareSystem.getStatus().get('dispenser')}")
    print(f"Cable stock          : {stock_of(inventory, 'cable')}")
    print(f"Transactions (sim)   : {len(payment.getTransactionHistory())}")
    print(f"Refunds triggered    : {payment.refund_count}")


if __name__ == "__main__":
    section("Aura Retail OS - Structured Path B Simulation")

    step(
        1,
        "Build subsystems",
        [
            "Inventory with simple products and a bundle",
            "In-memory payment system (deterministic)",
            "Hardware abstraction with Spiral dispenser",
            "Core system and customer session",
        ],
    )

    inventory, cable_product = build_inventory()
    payment = SimulatedPaymentSystem()
    hw = HardwareAbstraction(SpiralDispenser())
    core = KioskCoreSystem(
        inventorySystem=inventory,
        paymentSystem=payment,
        hardwareSystem=hw,
        kioskType="SIM_DEMO",
    )

    SessionManager().startSession("SIM01")
    state_snapshot(core, payment, inventory, "Post-bootstrap")

    checkpoint("Initial cable stock", stock_of(inventory, "cable") == 10, f"stock={stock_of(inventory, 'cable')}")

    section("Scenario 1: Successful Purchase")
    step(
        2,
        "Execute successful purchase",
        [
            "Input: product=USB-C Cable, qty=1, method=WALLET",
            "Expected: payment success, hardware dispense success, stock decrement",
        ],
    )
    tx_before = len(payment.getTransactionHistory())
    ok_purchase = core.executeCommand(PurchaseCommand(cable_product, 1, "WALLET"))
    print_new_transaction(payment, tx_before)
    checkpoint("Purchase command succeeded", ok_purchase)
    checkpoint("Stock decreased by 1", stock_of(inventory, "cable") == 9, f"stock={stock_of(inventory, 'cable')}")
    state_snapshot(core, payment, inventory, "After successful purchase")

    section("Scenario 2: Atomic Rollback on Hardware Failure")
    step(
        3,
        "Inject hardware failure and verify rollback",
        [
            "Action: jam USB-C Cable slot",
            "Input: product=USB-C Cable, qty=1, method=WALLET",
            "Expected: purchase fails, refund triggers, stock restored, core enters ERROR",
        ],
    )
    pre_stock = stock_of(inventory, "cable")
    hw.toggleProductJam("USB-C Cable")
    tx_before = len(payment.getTransactionHistory())
    failed_purchase = core.executeCommand(PurchaseCommand(cable_product, 1, "WALLET"))
    post_stock = stock_of(inventory, "cable")
    print_new_transaction(payment, tx_before)
    hw.toggleProductJam("USB-C Cable")

    checkpoint("Purchase failed as expected", not failed_purchase)
    checkpoint("Stock restored after rollback", pre_stock == post_stock, f"before={pre_stock}, after={post_stock}")
    checkpoint("Refund was triggered", payment.refund_count >= 1, f"refund_count={payment.refund_count}")
    checkpoint("Core moved to ERROR state", core.getSystemStatus() == "ERROR", f"status={core.getSystemStatus()}")
    state_snapshot(core, payment, inventory, "After rollback scenario")

    # Restore for next scenario
    step(4, "Recover core status for next scenario", ["Action: set system status back to ACTIVE"])
    core.setSystemStatus("ACTIVE")
    state_snapshot(core, payment, inventory, "After recovery")

    section("Scenario 3: Runtime Hot-Swap")
    step(
        5,
        "Perform runtime hot-swap",
        [
            "Start a long-running command (simulated in-flight operation)",
            "Call replaceDispenser(RoboticDispenser)",
            "Expected: system waits for in-flight command, then swaps dispenser",
        ],
    )
    long_cmd = LongRunningCommand(duration_s=1.2)
    worker = threading.Thread(target=lambda: core.executeCommand(long_cmd), daemon=True)
    worker.start()

    start = time.time()
    swapped = core.replaceDispenser(RoboticDispenser(), timeout=5.0)
    elapsed = time.time() - start
    worker.join()

    status = core.hardwareSystem.getStatus()
    checkpoint("Hot-swap succeeded", swapped)
    checkpoint("Dispenser switched to ROBOT", "ROBOT" in status.get("dispenser", ""), str(status))
    checkpoint("Hot-swap waited for in-flight command", elapsed >= 1.0, f"elapsed={elapsed:.2f}s")
    state_snapshot(core, payment, inventory, "After hot-swap")

    step(6, "Final verification", ["Validate final stable system state and summarize metrics"])

    print_summary(core, payment, inventory)
    print("\nSimulation complete.")
