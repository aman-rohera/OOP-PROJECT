"""
hardware/failure_handler.py
Abstract base for the hardware failure handling chain.

Pattern: Chain of Responsibility (Abstract Handler)
Member responsibility: Vivek
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Callable


class FailureHandler(ABC):
    """
    Abstract Handler in the chain.

    Design Pattern: Chain of Responsibility
    Each handler tries to resolve a hardware failure.
    If it cannot, it forwards to the next handler in the chain.
    Chain: RetryHandler → RecalibrationHandler → TechnicianAlertHandler
    """

    def __init__(self):
        self._next: Optional[FailureHandler] = None

    def set_next(self, handler: FailureHandler) -> FailureHandler:
        """Attach the next handler; returns it to allow fluent chaining."""
        self._next = handler
        return handler

    @abstractmethod
    def handle(self, failure: dict, log_cb: Optional[Callable] = None) -> dict:
        """
        Try to handle the failure.
        Args:
            failure: dict with keys: component, error_message, severity
            log_cb:  optional callback(str) for GUI event log
        Returns:
            dict with resolved: bool, handler: str, message: str
        """
        pass

    @abstractmethod
    def get_handler_name(self) -> str:
        pass

    def _forward(self, failure: dict, log_cb: Optional[Callable]) -> dict:
        """Pass to next handler or declare unresolved if end of chain."""
        if self._next:
            return self._next.handle(failure, log_cb)
        return {"resolved": False, "handler": "EndOfChain",
                "message": "All handlers exhausted. Manual intervention required."}
