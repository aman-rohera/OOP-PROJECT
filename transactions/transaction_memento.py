"""
transactions/transaction_memento.py
Stores a snapshot of inventory state before a transaction.

Pattern: Memento
  - Originator: Kiosk / PurchaseItemCommand
  - Memento: TransactionMemento
  - Caretaker: CommandInvoker

Member responsibility: Diya
"""
from dataclasses import dataclass
from typing import Dict


@dataclass
class TransactionMemento:
    """
    Snapshot of inventory state at the moment a transaction begins.
    Allows rollback if the transaction fails mid-way (e.g. dispenser fault).

    Design Pattern: Memento
    """
    transaction_id: str
    inventory_snapshot: Dict[str, int]
    product_id: str
    quantity: int
    amount: float
    timestamp: str

    def get_snapshot(self) -> Dict[str, int]:
        """Return a copy of the saved inventory snapshot."""
        return dict(self.inventory_snapshot)

    def __str__(self):
        return f"Memento[{self.transaction_id}] @ {self.timestamp}"
