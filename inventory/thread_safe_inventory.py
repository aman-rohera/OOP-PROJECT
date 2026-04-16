"""
inventory/thread_safe_inventory.py
Thread-safe wrapper for inventory operations to handle concurrent transactions.

Pattern: Decorator/Wrapper
Responsibility: Ensure atomic operations on inventory, prevent race conditions
"""
import threading
from typing import Dict, List, Optional


class ThreadSafeInventory:
    """
    Thread-safe wrapper around InventoryManager.
    
    Uses locks to ensure that concurrent transactions don't oversell products.
    All critical operations are protected by mutex locks.
    """
    
    def __init__(self, inventory_manager):
        """
        Initialize thread-safe inventory wrapper.
        
        Args:
            inventory_manager: The underlying InventoryManager instance
        """
        self.inventory_manager = inventory_manager
        self._lock = threading.RLock()  # Reentrant lock for nested calls
        self._product_locks: Dict[str, threading.Lock] = {}
        
        # Create per-product locks for fine-grained locking
        for product in inventory_manager.get_all_products():
            self._product_locks[product["id"]] = threading.Lock()
    
    def _get_product_lock(self, product_id: str) -> threading.Lock:
        """Get or create lock for a specific product."""
        with self._lock:
            if product_id not in self._product_locks:
                self._product_locks[product_id] = threading.Lock()
            return self._product_locks[product_id]
    
    # ── Read operations (no lock needed for simple reads) ────────────────
    
    def get_product(self, product_id: str) -> Optional[dict]:
        """Get product information."""
        return self.inventory_manager.get_product(product_id)
    
    def get_all_products(self) -> List[dict]:
        """Get all products."""
        return self.inventory_manager.get_all_products()
    
    def get_available_stock(self, product_id: str) -> int:
        """Get available stock for a product."""
        with self._get_product_lock(product_id):
            return self.inventory_manager.get_available_stock(product_id)
    
    def get_low_stock_products(self, threshold: int = 10) -> List[dict]:
        """Get products with low stock."""
        with self._lock:
            return self.inventory_manager.get_low_stock_products(threshold)
    
    # ── Write operations (require locks) ───────────────────────────────
    
    def reserve(self, product_id: str, quantity: int) -> bool:
        """
        Atomically reserve stock during transaction.
        
        Thread-safe: Lock product for exclusive access during check-and-update.
        """
        with self._get_product_lock(product_id):
            # Check if available
            if self.inventory_manager.get_available_stock(product_id) >= quantity:
                return self.inventory_manager.reserve(product_id, quantity)
            return False
    
    def release(self, product_id: str, quantity: int) -> None:
        """
        Atomically release reserved stock.
        
        Thread-safe: Release lock prevents double-release.
        """
        with self._get_product_lock(product_id):
            self.inventory_manager.release(product_id, quantity)
    
    def deduct(self, product_id: str, quantity: int) -> bool:
        """
        Atomically deduct stock after purchase commit.
        
        Thread-safe: Lock prevents concurrent modifications.
        """
        with self._get_product_lock(product_id):
            return self.inventory_manager.deduct(product_id, quantity)
    
    def restock(self, product_id: str, quantity: int) -> bool:
        """
        Atomically add stock during restocking.
        
        Thread-safe: Lock prevents concurrent modifications.
        """
        with self._get_product_lock(product_id):
            return self.inventory_manager.restock(product_id, quantity)
    
    def set_hardware_unavailable(self, product_id: str, state: bool) -> None:
        """Mark product as hardware-unavailable."""
        with self._get_product_lock(product_id):
            self.inventory_manager.set_hardware_unavailable(product_id, state)
    
    # ── Admin operations (use global lock for data consistency) ─────────
    
    def add_product(self, product: dict) -> bool:
        """Add a new product (Admin operation)."""
        with self._lock:
            result = self.inventory_manager.add_product(product)
            if result:
                self._product_locks[product["id"]] = threading.Lock()
            return result
    
    def remove_product(self, product_id: str) -> bool:
        """Remove a product (Admin operation)."""
        with self._lock:
            return self.inventory_manager.remove_product(product_id)
    
    def add_stock(self, product_id: str, quantity: int) -> bool:
        """Add stock to a product (Admin operation)."""
        with self._get_product_lock(product_id):
            return self.inventory_manager.add_stock(product_id, quantity)
    
    # ── Snapshot operations ────────────────────────────────────────────
    
    def get_snapshot(self) -> Dict[str, int]:
        """Get stock snapshot for rollback."""
        with self._lock:
            return self.inventory_manager.get_snapshot()
    
    def restore_snapshot(self, snapshot: Dict[str, int]) -> None:
        """Restore from snapshot."""
        with self._lock:
            self.inventory_manager.restore_snapshot(snapshot)
