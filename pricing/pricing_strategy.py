"""
pricing/pricing_strategy.py
Abstract base class for all pricing strategies.

Pattern: Strategy (Abstract Strategy)
  - Defines the interface for all concrete pricing algorithms.
  - Kiosk holds a reference to a PricingStrategy and delegates
    price calculation to it — allowing runtime strategy swaps.

"""
from abc import ABC, abstractmethod


class PricingStrategy(ABC):
    """
    Abstract Strategy — all pricing algorithms implement this interface.

    Design Pattern: Strategy
    Allows the kiosk to switch pricing behavior at runtime without
    changing the kiosk's own code (Open/Closed Principle).
    """

    @abstractmethod
    def calculate_price(self, base_price: float) -> float:
        """Compute the final sale price from the item's base price."""
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Human-readable name for the UI."""
        pass

    @abstractmethod
    def get_multiplier(self) -> float:
        """Price multiplier relative to base price."""
        pass

    def get_description(self) -> str:
        pct = int((self.get_multiplier() - 1) * 100)
        sign = "+" if pct >= 0 else ""
        return f"{self.get_strategy_name()} Pricing ({sign}{pct}%)"
