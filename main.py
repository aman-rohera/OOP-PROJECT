"""
main.py — Entry point for Aura Retail OS.

Boots the system:
  1. Show kiosk selection screen (Factory pattern)
  2. Load config + inventory from JSON (persistence)
  3. Initialize CentralRegistry (Singleton)
  4. Create EventBus + subscriber services (Observer)
  5. Create Kiosk via selected factory (Abstract Factory)
  6. Wrap in KioskInterface (Facade)
  7. Launch Tkinter GUI with Admin features
"""
import sys
import os
import tkinter as tk

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(__file__))

from core.central_registry import CentralRegistry
from core.kiosk_factory import GeneralKioskFactory, PharmacyKioskFactory, EmergencyReliefKioskFactory
from core.kiosk_interface import KioskInterface
from events.event_system import EventBus
from events.subscribers import MaintenanceService, SupplyChainSystem, CityMonitoringCenter
from persistence.data_manager import DataManager
from gui.app import AuraRetailOSApp
from gui.kiosk_selection import KioskSelectionScreen


def main():
    # 0. Show kiosk selection screen
    root = tk.Tk()
    selection_screen = KioskSelectionScreen(root)
    root.mainloop()
    root.destroy()
    
    kiosk_type = selection_screen.get_selected_kiosk()
    
    if not kiosk_type:
        return  # User closed without selecting
    
    # 1. Load persisted data
    config = DataManager.load_config()
    products = DataManager.load_inventory_for_kiosk(kiosk_type)

    # 2. Initialize the Singleton registry
    registry = CentralRegistry()
    registry.initialize(config)

    # 3. Create EventBus (Observer hub)
    event_bus = EventBus()

    # 4. Wire up subscriber services (Concrete Observers)
    #    GUI callbacks will be registered after app creation
    maintenance_svc = MaintenanceService(event_bus)
    supply_chain    = SupplyChainSystem(event_bus)
    city_monitor    = CityMonitoringCenter(event_bus)

    # 5. Build kiosk via Abstract Factory (selected type)
    if kiosk_type == "food":
        factory = GeneralKioskFactory()
    elif kiosk_type == "pharmacy":
        factory = PharmacyKioskFactory()
    elif kiosk_type == "emergency":
        factory = EmergencyReliefKioskFactory()
    else:
        factory = GeneralKioskFactory()
    
    kiosk = factory.create_kiosk(products, event_bus)

    # 6. Wrap in Facade
    ki = KioskInterface(
        kiosk,
        registry,
        data_manager=DataManager,
        kiosk_type=kiosk_type,
    )

    # 7. Launch GUI
    app = AuraRetailOSApp(ki, registry)

    # Wire subscriber GUI callbacks after app is created
    maintenance_svc.gui_callback = app._log
    supply_chain.gui_callback    = app._log
    city_monitor.gui_callback    = app._log

    app.run()


if __name__ == "__main__":
    main()
