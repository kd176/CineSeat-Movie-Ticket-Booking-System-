"""
LIFO Stack for Booking Rollback, Undo & Cancellation History
Module: dsa.cancellation_stack
Academic Concept: Stack Data Structure, LIFO (Last-In-First-Out), Transaction Rollback

Time Complexity:
- Push: O(1)
- Pop: O(1)
- Peek: O(1)
Space Complexity: O(N)
"""

import time
from typing import List, Dict, Any, Optional


class BookingAction:
    def __init__(self, action_type: str, order_id: int, user_id: str, snapshot: Dict[str, Any]):
        self.action_type = action_type      # "BOOKING_CREATED", "BOOKING_CANCELLED", "SEATS_RELEASED"
        self.order_id = order_id
        self.user_id = user_id
        self.snapshot = snapshot            # Contains booked seats, show key, amount
        self.timestamp = time.time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "actionType": self.action_type,
            "orderId": self.order_id,
            "userId": self.user_id,
            "snapshot": self.snapshot,
            "timestamp": self.timestamp
        }


class BookingHistoryStack:
    """
    LIFO Stack tracking audit history and facilitating order rollbacks / cancellations.
    When a booking is cancelled, the action record is pushed onto this stack.
    """

    def __init__(self, max_capacity: int = 1000):
        self._items: List[BookingAction] = []
        self.max_capacity = max_capacity

    def push(self, action: BookingAction) -> None:
        """Push an action onto the top of the stack in O(1) time."""
        if len(self._items) >= self.max_capacity:
            self._items.pop(0)  # Evict oldest entry if capacity reached
        self._items.append(action)

    def pop(self) -> Optional[BookingAction]:
        """Pop the most recent action from the top of the stack in O(1) time."""
        if not self._items:
            return None
        return self._items.pop()

    def peek(self) -> Optional[BookingAction]:
        """Inspect the top of the stack in O(1) time."""
        return self._items[-1] if self._items else None

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)

    def get_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Return history in reverse chronological order (most recent first)."""
        return [action.to_dict() for action in reversed(self._items[-limit:])]
