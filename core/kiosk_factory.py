"""
core/kiosk_factory.py
Abstract Factory for creating different kiosk types.

Pattern: Abstract Factory
"""
from abc import ABC, abstractmethod
from core.kiosk import Kiosk
from inventory.inventory_manager import InventoryManager
from events.event_system import EventBus
from pricing.standard_pricing import StandardPricing
from pricing.emergency_pricing import EmergencyPricing
from state.active_state import ActiveState
from state.emergency_state import EmergencyLockdownState
from hardware.retry_handler import RetryHandler
from hardware.recalibration_handler import RecalibrationHandler
from hardware.technician_handler import TechnicianAlertHandler


def build_failure_chain() -> RetryHandler:
    """Assemble the Chain of Responsibility: Retry → Recalibrate → Technician."""
    retry = RetryHandler(max_retries=3)
    recal = RecalibrationHandler()
    tech = TechnicianAlertHandler()
    retry.set_next(recal).set_next(tech)
    return retry


class KioskFactory(ABC):
    """Abstract Factory — each subclass creates a fully configured Kiosk."""

    @abstractmethod
    def create_kiosk(self, products: list, event_bus: EventBus) -> Kiosk:
        pass


class GeneralKioskFactory(KioskFactory):
    """Creates a standard general-purpose kiosk."""

    def create_kiosk(self, products: list, event_bus: EventBus) -> Kiosk:
        return Kiosk(
            kiosk_id="AURA-001",
            name="Aura Kiosk Alpha",
            location="Metro Station Central",
            inventory_manager=InventoryManager(products),
            event_bus=event_bus,
            initial_state=ActiveState(),
            initial_pricing_strategy=StandardPricing(),
            failure_chain=build_failure_chain()
        )


class PharmacyKioskFactory(KioskFactory):
    """Creates a kiosk configured for pharmacy / hospital environments."""

    def create_kiosk(self, products: list, event_bus: EventBus) -> Kiosk:
        return Kiosk(
            kiosk_id="AURA-PH-001",
            name="Pharmacy Kiosk",
            location="City Hospital",
            inventory_manager=InventoryManager(products),
            event_bus=event_bus,
            initial_state=ActiveState(),
            initial_pricing_strategy=StandardPricing(),
            failure_chain=build_failure_chain()
        )


class EmergencyReliefKioskFactory(KioskFactory):
    """Creates a kiosk pre-configured for emergency/disaster zones."""

    def create_kiosk(self, products: list, event_bus: EventBus) -> Kiosk:
        return Kiosk(
            kiosk_id="AURA-EM-001",
            name="Emergency Relief Kiosk",
            location="Disaster Zone Alpha",
            inventory_manager=InventoryManager(products),
            event_bus=event_bus,
            initial_state=EmergencyLockdownState(max_per_person=2),
            initial_pricing_strategy=EmergencyPricing(surge_rate=0.5),
            failure_chain=build_failure_chain()
        )
