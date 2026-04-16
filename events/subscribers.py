"""
events/subscribers.py
Concrete Observer classes for the Aura Retail OS event system.

Pattern: Observer (Concrete Observers)
  - MaintenanceService   → listens for HardwareFailureEvent
  - SupplyChainSystem    → listens for LowStockEvent
  - CityMonitoringCenter → listens for all critical events
"""
from events.events import (
    LowStockEvent, HardwareFailureEvent, EmergencyModeActivatedEvent,
    ModeChangedEvent, TransactionEvent
)


class MaintenanceService:
    """
    Observer: responds to hardware failure events.
    Pattern: Observer (Concrete Observer)
    Member responsibility: Vivek
    """

    def __init__(self, event_bus, gui_callback=None):
        self.failure_log = []
        self.gui_callback = gui_callback
        # Register as observer
        event_bus.subscribe(HardwareFailureEvent, self.on_hardware_failure)

    def on_hardware_failure(self, event: HardwareFailureEvent):
        self.failure_log.append({
            "time": event.timestamp,
            "component": event.component,
            "error": event.error_message,
            "severity": event.severity
        })
        print(f"[MaintenanceService] Hardware alert: {event.component} — {event.error_message}")
        if self.gui_callback:
            self.gui_callback(f"🔧 Maintenance alerted: {event.component} failure ({event.severity})")


class SupplyChainSystem:
    """
    Observer: responds to low stock events and triggers reorder.
    Pattern: Observer (Concrete Observer)
    Member responsibility: Vivek
    """

    def __init__(self, event_bus, gui_callback=None):
        self.restock_requests = []
        self.gui_callback = gui_callback
        # Register as observer
        event_bus.subscribe(LowStockEvent, self.on_low_stock)

    def on_low_stock(self, event: LowStockEvent):
        self.restock_requests.append({
            "time": event.timestamp,
            "product_id": event.product_id,
            "product_name": event.product_name,
            "quantity": event.remaining_quantity
        })
        print(f"[SupplyChain] Restock order for: {event.product_name}")
        if self.gui_callback:
            self.gui_callback(f"📦 Supply chain: Reorder placed for {event.product_name}")


class CityMonitoringCenter:
    """
    Observer: city-wide monitoring — tracks emergencies and critical events.
    Pattern: Observer (Concrete Observer)
    Member responsibility: Vivek
    """

    def __init__(self, event_bus, gui_callback=None):
        self.alerts = []
        self.gui_callback = gui_callback
        # Subscribe to multiple event types
        event_bus.subscribe(EmergencyModeActivatedEvent, self.on_emergency)
        event_bus.subscribe(ModeChangedEvent, self.on_mode_changed)
        event_bus.subscribe(HardwareFailureEvent, self.on_hardware_failure)

    def on_emergency(self, event: EmergencyModeActivatedEvent):
        self.alerts.append(str(event))
        print(f"[CityMonitor] 🚨 EMERGENCY at {event.location}: {event.reason}")
        if self.gui_callback:
            self.gui_callback(f"🏙 City Monitor: Emergency reported — {event.reason}")

    def on_mode_changed(self, event: ModeChangedEvent):
        self.alerts.append(str(event))
        print(f"[CityMonitor] Mode change: {event.old_mode} → {event.new_mode}")

    def on_hardware_failure(self, event: HardwareFailureEvent):
        if event.severity in ("high", "critical"):
            self.alerts.append(str(event))
            if self.gui_callback:
                self.gui_callback(f"🏙 City Monitor: Critical — {event.component} failed")
