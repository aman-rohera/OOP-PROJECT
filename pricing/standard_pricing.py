"""
pricing/standard_pricing.py
Standard pricing — charges the base price (1x multiplier).

Pattern: Strategy (Concrete Strategy)
"""
from pricing.pricing_strategy import PricingStrategy


class StandardPricing(PricingStrategy):
    """Standard prices — no modification to base_price."""

    def calculate_price(self, base_price: float) -> float:
        return round(base_price, 2)

    def get_strategy_name(self) -> str:
        return "Standard"

    def get_multiplier(self) -> float:
        return 1.0
