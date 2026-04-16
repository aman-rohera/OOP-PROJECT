"""
state/maintenance_state.py — Kiosk under maintenance, no purchases.
Pattern: State (Concrete State) | Member: Team Member 2
"""
from state.kiosk_state import KioskState


class MaintenanceState(KioskState):
    """Maintenance mode — technicians can restock; purchases blocked."""

    def handle_purchase(self, kiosk, product_id, quantity):
        return {"allowed": False, "message": "❌ Kiosk under maintenance. Purchases unavailable.", "max_quantity": None}

    def handle_restock(self, kiosk, product_id, quantity):
        return {"allowed": True, "message": "Restocking allowed during maintenance."}

    def handle_diagnostics(self, kiosk):
        return {"status": "maintenance", "mode": self.get_mode_name(), "message": "Running hardware diagnostics..."}

    def get_mode_name(self): return "Maintenance"
    def can_purchase(self): return False
    def get_status_color(self): return "#747EE0"  # purple
