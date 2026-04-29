# Aura Retail OS

> **A Smart Vending Machine System** built with Python. This project shows how to build a complex system using clean coding principles (OOP) that is easy to understand, change, and expand.

---

## 📋 Table of Contents

- [What is Aura?](#what-is-aura)
- [Cool Features](#cool-features)
- [How it's Organized](#how-its-organized)
- [Coding Patterns Used](#coding-patterns-used)
- [Getting Started](#getting-started)
- [Security & Maintenance](#security--maintenance)
- [The Team](#the-team)

---

## What is Aura?

**Aura Retail OS** is a terminal-based program that acts like a real-world self-service kiosk. It was built for an Object-Oriented Programming course. Instead of just selling snacks, it can be configured to sell medicine, tech gear, or even emergency supplies for disaster relief.

---

## Cool Features

| Feature | What it does |
|---|---|
| **Vending Presets** | Change the machine to a Food, Pharmacy, or Tech shop in one click. |
| **Smart Buying** | Checks if items are in stock and if the right hardware is active before selling. |
| **Simple Refunds** | Easily give money back for items bought in the current session. |
| **Hardware Simulation** | Acts like real hardware with robotic arms and dispensers. |
| **Dynamic Prices** | Prices can change automatically (e.g., lower prices in emergencies). |
| **Admin Panel** | A secret menu for owners to restock items and check system health. |
| **Technician Tools** | A special menu to test hardware and add modules like Solar Panels. |
| **Premium Look** | Uses colors and boxes to look like a professional modern terminal. |

---

## How it's Organized

We split the code into different folders to keep things tidy:

```text
Project/
│
├── main.py                         # The main entry point to start the system
│
├── admin/
│   └── adminTerminal.py            # The secret menu for owners (needs a PIN)
│
├── core/                           # The "brain" of the system
│   ├── bootstrapper.py             # Handles the startup process
│   ├── kioskCoreSystem.py          # Runs the main logic and commands
│   ├── kioskInterface.py           # A simple way for the UI to talk to the brain
│   └── commands/                   # Individual actions like Buy, Refund, and Restock
│
├── factory/                        # Used to create different types of kiosks
│
├── hardware/                       # Controls the simulated motors and sensors
│   └── modules/                    # Add-ons like Solar Panels or 5G Network
│
├── inventory/                      # Manages products, bundles, and pricing
│
├── monitoring/                     # Keeps a log of everything that happens
│
├── payment/                        # Handles UPI, Card, and Wallet payments
│
├── persistence/                    # Saves your data to files so it's not lost
│
└── registry/                       # Stores the system's settings in one place
```

---

## Coding Patterns Used

This project uses **10 common design patterns** to keep the code clean:

1.  **Abstract Factory**: To build different kiosk types (like Food vs. Pharmacy) easily.
2.  **Command**: To turn actions like "Buy" into objects that can be logged or undone.
3.  **Decorator**: To "wrap" the machine with extra features like Solar Power.
4.  **Strategy**: To swap pricing rules (Standard vs. Emergency) on the fly.
5.  **Observer**: To let the system know when something happens (like a hardware error).
6.  **Facade**: To give the UI a simple set of buttons to press.
7.  **Adapter**: To make different payment types (UPI, Card) work the same way.
8.  **Proxy**: To add security checks before accessing inventory or hardware.
9.  **Singleton**: To make sure there is only one "Settings" object in the whole app.
10. **Composite**: To group items together into "Bundles" and treat them as one product.

---

## Security & Maintenance

Aura includes a **Field Service Console** for technicians. You need a Technician ID to get in.

*   **Change Parts**: Swap out the vending mechanism (Robotic Arm vs. Spiral).
*   **Add Power**: Deploy Solar Panels or turn on Refrigeration.
*   **Fix Jams**: See which product slots are stuck and fix them.

---

## Getting Started

### What you need
- **Python 3.10** or newer.
- A modern terminal (like Windows Terminal or VS Code Terminal) for colors to work.

### How to run it
1. Open your terminal in the project folder.
2. Type `python main.py` and press Enter.
3. Follow the on-screen instructions to pick your kiosk and start buying!

---

## Working Simulation
<img width="1920" height="1200" alt="Screenshot 2026-04-11 174209" src="https://github.com/user-attachments/assets/9dedc000-9044-45d4-9cc4-7227fbab7260" />
<img width="1920" height="1200" alt="Screenshot 2026-04-11 174246" src="https://github.com/user-attachments/assets/27f2f199-3d5e-4239-abe9-c7d4934c724e" />
<img width="1920" height="1200" alt="Screenshot 2026-04-11 174306" src="https://github.com/user-attachments/assets/8a0461de-431f-46b2-a156-7527baf6da89" />
<img width="1920" height="1200" alt="Screenshot 2026-04-11 174343" src="https://github.com/user-attachments/assets/1fc84fbf-fed2-48ec-9dfd-b10667ad98c0" />
<img width="1920" height="1200" alt="Screenshot 2026-04-11 174407" src="https://github.com/user-attachments/assets/6fa13391-2e1f-4636-9032-9ce0044b7695" />

---

## The Team

- **Course**: IT620 – Object-Oriented Programming
- **Semester**: Semester 2
- **Team Name**: Oops, We Did It Again!
- **Members**:
  - Maryam Shaikh
  - Manushree Thakkar
  - Anistina Dsouza
  - Ruchita Patadiya

---

*Built with passion and clean code.*
