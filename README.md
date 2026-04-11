# Aura Retail OS

> **A Smart Automated Retail Kiosk System** built with Python, demonstrating core Object-Oriented Programming principles through a fully simulated retail environment.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [OOP Design Patterns](#oop-design-patterns)
- [Getting Started](#getting-started)
- [Team](#team)

---

## Overview

**Aura Retail OS** is a terminal-based kiosk management system developed as a group project for **IT620 – Object-Oriented Programming**. It simulates a real-world automated retail kiosk, supporting purchasing, refunding, inventory restocking, and system diagnostics — all driven by clean OOP architecture.

---

## Features

| Feature | Description |
|---|---|
| **Purchase Items** | Browse available products, select quantity, and pay via UPI, Card, or Wallet |
| **Refund Transactions** | Process refunds through the same payment method used at purchase |
| **Restock Inventory** | Add stock to existing products through the kiosk interface |
| **System Diagnostics** | View real-time system status and command execution history |
| **Premium Terminal UI** | Colored ASCII box interface for a professional kiosk look and feel |
| **Inventory Proxy** | Security logging layer for all inventory access |

---

## Project Structure

```
Project/
│
├── main.py                         # Entry point — UI screens & kiosk loop
│
├── core/                           # Core system logic
│   ├── kiosk_core_system.py        # Central command executor & state manager
│   ├── kioskInterface.py           # High-level facade for all kiosk operations
│   └── commands/                   # Command Pattern implementations
│       ├── command.py              # Abstract base Command class
│       ├── purchase_command.py     # Handles full purchase flow
│       ├── refund_command.py       # Handles refund processing
│       └── restock_command.py      # Handles inventory restocking
│
├── models/
│   └── productModel.py             # Plain data model for a product (id, name, price, stock)
│
├── inventory/
│   ├── components/
│   │   ├── product.py              # Abstract base class for all products
│   │   ├── simpleProduct.py        # Concrete product wrapping ProductModel
│   │   └── inventoryManager.py     # Utility for displaying inventory
│   └── security/
│       └── inventoryProxy.py       # Proxy pattern — security logging for inventory access
│
├── payment/
│   ├── payment_system.py           # Payment facade routing to adapters
│   ├── interfaces/
│   │   └── payment_processor.py   # Abstract interface for all payment processors
│   └── adapters/
│       ├── upi_adapter.py          # UPI payment adapter
│       ├── card_adapter.py         # Card payment adapter
│       └── wallet_adapter.py       # Wallet payment adapter
│
├── hardware/                       # Hardware abstraction layer (extensible)
│   ├── dispensers/
│   ├── interfaces/
│   └── modules/
│
├── monitoring/                     # System monitoring (extensible)
├── persistence/                    # Data persistence (extensible)
├── registry/                       # Component registry (extensible)
└── utils/                          # Utility helpers (extensible)
```

---

## OOP Design Patterns

This project is a practical demonstration of **5 core OOP design patterns**:

### 1. Command Pattern

Each user action (purchase, refund, restock) is encapsulated as a `Command` object. The `KioskCoreSystem` executes these commands uniformly, logs them to history, and handles errors centrally.

```
Command (base)
├── PurchaseCommand
├── RefundCommand
└── RestockCommand
```

### 2. Facade Pattern

`KioskInterface` acts as a simplified front door to the complex core system. The UI only calls `purchaseItem()`, `refundTransaction()`, or `restockInventory()` — without knowing how commands are created or dispatched.

### 3. Adapter Pattern

Each payment method (UPI, Card, Wallet) has a different internal API, but all are adapted to a common `PaymentProcessor` interface. `PaymentSystem` selects the right adapter at runtime.

```
PaymentProcessor (interface)
├── UPIAdapter
├── CardAdapter
└── WalletAdapter
```

### 4. Abstraction & Inheritance

`Product` is an abstract base class (ABC) enforcing a contract across all product types. `SimpleProduct` inherits from `Product` and composes a `ProductModel` (data) — cleanly separating behaviour from data.

---

## Getting Started

### Prerequisites

- Python **3.8+**
- No external libraries required — uses only the Python standard library

### Running the Kiosk

```bash
# Navigate to the project directory

# Run the kiosk
python main.py
```

> **Note:** ANSI color codes are used for the terminal UI. Run in **Windows Terminal**, **PowerShell**, or any terminal that supports ANSI escape sequences for the best experience.

---

## Working Simulation
<img width="1920" height="1200" alt="Screenshot 2026-04-11 174209" src="https://github.com/user-attachments/assets/9dedc000-9044-45d4-9cc4-7227fbab7260" />
<img width="1920" height="1200" alt="Screenshot 2026-04-11 174246" src="https://github.com/user-attachments/assets/27f2f199-3d5e-4239-abe9-c7d4934c724e" />
<img width="1920" height="1200" alt="Screenshot 2026-04-11 174306" src="https://github.com/user-attachments/assets/8a0461de-431f-46b2-a156-7527baf6da89" />
<img width="1920" height="1200" alt="Screenshot 2026-04-11 174343" src="https://github.com/user-attachments/assets/1fc84fbf-fed2-48ec-9dfd-b10667ad98c0" />
<img width="1920" height="1200" alt="Screenshot 2026-04-11 174407" src="https://github.com/user-attachments/assets/6fa13391-2e1f-4636-9032-9ce0044b7695" />

---

## Team

> **Course:** IT620 – Object-Oriented Programming  
> **Semester:** Semester 2  
> **Team Name:** Oops, We Did It Again

---

*Built with and OOP principles.*
