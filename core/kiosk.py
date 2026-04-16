"""
core/kiosk.py
The central Kiosk class — context for State and Strategy patterns.

Member responsibility: Divyesh
"""
from inventory.inventory_manager import InventoryManager
from events.event_system import EventBus
from transactions.command import CommandInvoker
from hardware.failure_handler import FailureHandler


class Kiosk:
    """
    The core kiosk entity.

    Acts as the Context in:
      - State Pattern   → delegates to self.state
      - Strategy Pattern → delegates to self.pricing_strategy

    Holds references to:
      - InventoryManager
      - EventBus
      - CommandInvoker
      - FailureHandler chain
    """

    def __init__(self, kiosk_id: str, name: str, location: str,
                 inventory_manager: InventoryManager,
                 event_bus: EventBus,
                 initial_state,
                 initial_pricing_strategy,
                 failure_chain: FailureHandler = None):

        self.kiosk_id = kiosk_id
        self.name = name
        self.location = location
        self.inventory_manager = inventory_manager
        self.event_bus = event_bus
        self.state = initial_state
        self.pricing_strategy = initial_pricing_strategy
        self.failure_chain = failure_chain
        self.invoker = CommandInvoker()

    def set_state(self, new_state) -> None:
        """Transition to a new operating state (State Pattern)."""
        self.state = new_state

    def set_pricing_strategy(self, strategy) -> None:
        """Swap pricing strategy at runtime (Strategy Pattern)."""
        self.pricing_strategy = strategy

    def execute_command(self, command) -> dict:
        """Run a command through the invoker (Command Pattern)."""
        return self.invoker.execute(command)

    def undo_last(self) -> dict:
        return self.invoker.undo_last()

    def trigger_hardware_failure(self, component: str, error_msg: str,
                                  severity: str = "medium", log_cb=None) -> dict:
        """Process a hardware failure through the Chain of Responsibility."""
        if not self.failure_chain:
            return {"resolved": False, "message": "No failure handlers configured."}
        failure = {"component": component, "error_message": error_msg, "severity": severity}
        return self.failure_chain.handle(failure, log_cb)

    def __str__(self):
        return f"Kiosk[{self.kiosk_id}] @ {self.location} | Mode: {self.state}"
