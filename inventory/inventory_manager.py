"""
inventory/inventory_manager.py
Manages products, stock levels, reservations, and hardware availability.

Demonstrates: Encapsulation, Derived Attributes (project constraint)
  - Available stock is DERIVED: total − reserved − hardware_unavailable
  - Actual stock is never reduced until a transaction commits

Member responsibility: Aman
"""
from typing import Dict, List, Optional


class InventoryManager:
    """
    Central inventory manager for the kiosk.

    Derived attribute: available_stock = total − reserved
    (hardware-unavailable items are always treated as stock = 0)
    """

    def __init__(self, products: List[dict]):
        self._products: Dict[str, dict] = {}      # product_id -> product data
        self._reserved: Dict[str, int] = {}        # items held in active txns
        self._hw_unavailable: Dict[str, bool] = {} # marked unavailable by hardware

        for p in products:
            pid = p["id"]
            self._products[pid] = p.copy()
            self._reserved[pid] = 0
            self._hw_unavailable[pid] = False

    # ── Read ───────────────────────────────────────────────────────────────

    def get_product(self, product_id: str) -> Optional[dict]:
        return self._products.get(product_id)

    def get_all_products(self) -> List[dict]:
        return list(self._products.values())

    def get_available_stock(self, product_id: str) -> int:
        """Derived attribute: available = total - reserved (0 if hw fault)."""
        if self._hw_unavailable.get(product_id, False):
            return 0
        p = self._products.get(product_id)
        if not p:
            return 0
        return max(0, p["quantity"] - self._reserved.get(product_id, 0))

    def get_low_stock_products(self, threshold: int = 10) -> List[dict]:
        return [p for p in self._products.values() if p["quantity"] <= threshold]

    # ── Write ──────────────────────────────────────────────────────────────

    def reserve(self, product_id: str, quantity: int) -> bool:
        """Temporarily hold stock during an active transaction."""
        if self.get_available_stock(product_id) >= quantity:
            self._reserved[product_id] = self._reserved.get(product_id, 0) + quantity
            return True
        return False

    def release(self, product_id: str, quantity: int) -> None:
        """Release reserved stock (transaction cancelled or failed)."""
        self._reserved[product_id] = max(0, self._reserved.get(product_id, 0) - quantity)

    def deduct(self, product_id: str, quantity: int) -> bool:
        """Commit stock deduction after a successful purchase."""
        p = self._products.get(product_id)
        if not p:
            return False
        self.release(product_id, quantity)
        p["quantity"] -= quantity
        return True

    def restock(self, product_id: str, quantity: int) -> bool:
        p = self._products.get(product_id)
        if not p:
            return False
        p["quantity"] += quantity
        return True

    def set_hardware_unavailable(self, product_id: str, state: bool) -> None:
        self._hw_unavailable[product_id] = state

    # ── Snapshot (Memento support) ─────────────────────────────────────────

    def get_snapshot(self) -> Dict[str, int]:
        """Capture current stock levels for potential rollback."""
        return {pid: p["quantity"] for pid, p in self._products.items()}

    def restore_snapshot(self, snapshot: Dict[str, int]) -> None:
        """Restore stock from a previously captured snapshot."""
        for pid, qty in snapshot.items():
            if pid in self._products:
                self._products[pid]["quantity"] = qty

    def add_product(self, product: dict) -> bool:
        """Add a new product to inventory (Admin operation)."""
        if product["id"] in self._products:
            return False  # Product already exists
        self._products[product["id"]] = product.copy()
        self._reserved[product["id"]] = 0
        self._hw_unavailable[product["id"]] = False
        return True

    def remove_product(self, product_id: str) -> bool:
        """Remove a product from inventory (Admin operation)."""
        if product_id not in self._products:
            return False
        del self._products[product_id]
        del self._reserved[product_id]
        del self._hw_unavailable[product_id]
        return True

    def add_stock(self, product_id: str, quantity: int) -> bool:
        """Add stock to an existing product (Admin operation)."""
        p = self._products.get(product_id)
        if not p:
            return False
        p["quantity"] += quantity
        return True
