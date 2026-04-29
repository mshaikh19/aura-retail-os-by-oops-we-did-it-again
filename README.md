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





<table>
  <tr>
    <td><img width="1920" height="1200" alt="Screenshot (302)" src="https://github.com/user-attachments/assets/6466e97a-0a3e-4930-b52e-bd5197e32a43" /></td>
    <td><img width="1920" height="1200" alt="Screenshot (231)" src="https://github.com/user-attachments/assets/ad2f9908-e843-4bc5-b250-36091b3b61cf" /></td>
  </tr>

  <tr>
    <td><img width="1920" height="1200" alt="Screenshot (235)" src="https://github.com/user-attachments/assets/369db448-216d-462a-b220-1d131a5ab4d8" /></td>
    <td><img width="1920" height="1200" alt="Screenshot (237)" src="https://github.com/user-attachments/assets/4a7be175-4ac8-4664-b9ce-8bc8250c2fcf" /></td>
  </tr>

  <tr>
    <td><img width="1920" height="1200" alt="Screenshot (239)" src="https://github.com/user-attachments/assets/0ab79c57-d6fe-40e2-bbf1-b47ee8b4965c" /></td>
    <td><img width="1920" height="1200" alt="Screenshot (240)" src="https://github.com/user-attachments/assets/6a224990-3c9c-43e6-9740-bc86ffe45307" /></td>
  </tr>
  
  <tr>
    <td><img width="1920" height="1200" alt="Screenshot (242)" src="https://github.com/user-attachments/assets/b95136d5-79c3-4c20-999a-d5de58e45d0d" /></td>
    <td><img width="1920" height="1200" alt="Screenshot (244)" src="https://github.com/user-attachments/assets/dc22bba6-44e9-4919-b378-c98980be4146" /></td>
  </tr>

  <tr>
    <td><img width="1920" height="1200" alt="Screenshot (245)" src="https://github.com/user-attachments/assets/84746fad-0dd6-4357-ba42-e0a2f0c40691" /></td>
    <td><img width="1920" height="1200" alt="Screenshot (246)" src="https://github.com/user-attachments/assets/92dcb2c8-7104-49d0-980b-2b44967702eb" /></td>
  </tr>

  <tr>
    <td><img width="1920" height="1200" alt="Screenshot (247)" src="https://github.com/user-attachments/assets/3b7f2d6e-d8fc-4d7f-971e-0bc898da6b27" /></td>
    <td><img width="1920" height="1200" alt="Screenshot (251)" src="https://github.com/user-attachments/assets/eca14c25-a252-4f03-b1f3-e532d5b3e75c" /></td>
  </tr>

  <tr>
    <td><img width="1920" height="1200" alt="Screenshot (257)" src="https://github.com/user-attachments/assets/74dc7788-e49b-4993-9fee-be426f343850" /></td>
    <td><img width="1920" height="1200" alt="Screenshot (258)" src="https://github.com/user-attachments/assets/fe6496f8-b339-46e0-93c4-55c92a0c188e" /></td>
  </tr>

  <tr>
    <td><img width="1920" height="1200" alt="Screenshot (300)" src="https://github.com/user-attachments/assets/ca8c6715-ee51-4092-8062-40e9cf38bd44" /></td>
    <td><img width="1920" height="1200" alt="Screenshot (262)" src="https://github.com/user-attachments/assets/ab04d9a2-d5b5-4460-be2a-e36bb936f29d" /></td>
  </tr>

  <tr>
    <td><img width="1920" height="1200" alt="Screenshot (266)" src="https://github.com/user-attachments/assets/9ff3009d-a2d9-4fbb-abaf-22f54e43812c" /></td>
    <td><img width="1920" height="1200" alt="Screenshot (271)" src="https://github.com/user-attachments/assets/7fdff7d4-e864-4694-9719-3578cc0d7527" />
</td>
  </tr>

  <tr>
    <td><img width="1920" height="1200" alt="Screenshot (273)" src="https://github.com/user-attachments/assets/428baed1-6d76-427a-80d2-d0c1b4083533" /></td>
    <td><img width="1920" height="1200" alt="Screenshot (274)" src="https://github.com/user-attachments/assets/8e885651-41de-439c-af88-ff80231ff2aa" />
</td>
  </tr>

  <tr>
    <td><img width="1920" height="1200" alt="Screenshot (277)" src="https://github.com/user-attachments/assets/fe7d4bc7-cff9-43e8-8221-299aad7ff43f" /></td>
    <td><img width="1920" height="1200" alt="Screenshot (280)" src="https://github.com/user-attachments/assets/2ff4fda5-c85c-430b-85e6-ac0bc82cf394" /></td>
  </tr>

  <tr>
    <td><img width="1920" height="1200" alt="Screenshot (281)" src="https://github.com/user-attachments/assets/2523c4b5-12be-4162-8bd5-efd5394a1dff" /></td>
    <td><img width="1920" height="1200" alt="Screenshot (284)" src="https://github.com/user-attachments/assets/758e871c-bb47-4eb8-9961-e39a6d805830" /></td>
  </tr>
  <tr>
    <td><img width="1920" height="1200" alt="Screenshot (289)" src="https://github.com/user-attachments/assets/b396da5d-c865-47b9-8783-f13a9e4bb068" /></td>
    <td><img width="1920" height="1200" alt="Screenshot (292)" src="https://github.com/user-attachments/assets/68fb633a-d9a4-4fa0-829a-09400aa9bd75" /></td>
  </tr>
  <tr>
    <td colspan = 2><img width="1920" height="1200" alt="Screenshot (301)" src="https://github.com/user-attachments/assets/08f7dcc1-4d17-4e69-b006-92540e5d7b3b" /></td>
  </tr>
</table>
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

*Built with passion and OOPs!.*
