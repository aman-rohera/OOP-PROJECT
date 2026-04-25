"""
state/kiosk_state.py
Abstract base class for all kiosk operating states.

Pattern: State (Abstract State)
  - KioskState defines the interface for every concrete state.
  - The Kiosk class holds a reference to the current state and
    delegates all operations to it, enabling behavior changes
    simply by swapping the state object at runtime.

"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.kiosk import Kiosk


class KioskState(ABC):
    """
    Abstract State — each subclass represents one kiosk operating mode.

    Design Pattern: State
    Eliminates large if/elif chains for mode-based logic.
    Each state encapsulates its own purchase/restock/diagnostics rules.
    """

    @abstractmethod
    def handle_purchase(self, kiosk: Kiosk, product_id: str, quantity: int) -> dict:
        """Return a dict: {allowed: bool, message: str, max_quantity: int|None}"""
        pass

    @abstractmethod
    def handle_restock(self, kiosk: Kiosk, product_id: str, quantity: int) -> dict:
        """Return a dict: {allowed: bool, message: str}"""
        pass

    @abstractmethod
    def handle_diagnostics(self, kiosk: Kiosk) -> dict:
        """Return system diagnostic status dict."""
        pass

    @abstractmethod
    def get_mode_name(self) -> str:
        pass

    @abstractmethod
    def can_purchase(self) -> bool:
        pass

    @abstractmethod
    def get_status_color(self) -> str:
        """Return hex color string for GUI status indicator."""
        pass

    def __str__(self) -> str:
        return self.get_mode_name()
