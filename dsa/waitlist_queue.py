"""
FIFO Queue & Priority Queue for Waiting List Management
Module: dsa.waitlist_queue
Academic Concept: Doubly Linked List, FIFO Queue, Binary Min-Heap Priority Queue

Time Complexity:
- FIFO Enqueue / Dequeue: O(1)
- Priority Enqueue: O(log N)
- Priority Dequeue (Extract-Min): O(log N)
Space Complexity: O(N)
"""

import time
from typing import Optional, List, Dict, Any


class WaitlistRequest:
    """Represents a customer's request to wait for sold-out show seats."""

    def __init__(self, request_id: int, user_id: str, user_name: str, show_key: str, seat_count: int, priority: int = 10):
        self.request_id = request_id
        self.user_id = user_id
        self.user_name = user_name
        self.show_key = show_key
        self.seat_count = seat_count
        self.timestamp = time.time()
        self.priority = priority  # Lower number = higher priority (e.g., VIP = 1, Regular = 10)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "requestId": self.request_id,
            "userId": self.user_id,
            "userName": self.user_name,
            "showKey": self.show_key,
            "seatCount": self.seat_count,
            "timestamp": self.timestamp,
            "priority": self.priority,
        }


class Node:
    """Doubly linked list node for strict O(1) FIFO Queue."""
    def __init__(self, val: WaitlistRequest):
        self.val = val
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None


class FIFOQueue:
    """
    Custom Doubly Linked List implementation of a First-In-First-Out (FIFO) Queue.
    Guarantees strict fairness: earliest arrived group is at the head.
    """

    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        return self._size == 0

    def size(self) -> int:
        return self._size

    def enqueue(self, item: WaitlistRequest) -> None:
        """Add item to tail of queue in O(1) time."""
        new_node = Node(item)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self._size += 1

    def dequeue(self) -> Optional[WaitlistRequest]:
        """Remove and return item from head of queue in O(1) time."""
        if not self.head:
            return None
        val = self.head.val
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self._size -= 1
        return val

    def peek(self) -> Optional[WaitlistRequest]:
        """View front item without removing in O(1) time."""
        return self.head.val if self.head else None

    def to_list(self) -> List[Dict[str, Any]]:
        """Extract elements in queue order."""
        curr = self.head
        items = []
        pos = 1
        while curr:
            d = curr.val.to_dict()
            d["position"] = pos
            items.append(d)
            curr = curr.next
            pos += 1
        return items

    def remove_by_id(self, request_id: int) -> bool:
        """Remove a specific request when customer voluntarily leaves waitlist."""
        curr = self.head
        while curr:
            if curr.val.request_id == request_id:
                if curr.prev:
                    curr.prev.next = curr.next
                else:
                    self.head = curr.next

                if curr.next:
                    curr.next.prev = curr.prev
                else:
                    self.tail = curr.prev

                self._size -= 1
                return True
            curr = curr.next
        return False


class PriorityWaitlist:
    """
    Min-Heap Priority Queue implementation from scratch.
    Tuples are ordered by (priority, timestamp).
    Enables VIP/Loyalty member prioritized ticket allocation.
    """

    def __init__(self):
        self.heap: List[WaitlistRequest] = []

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    def size(self) -> int:
        return len(self.heap)

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left_child(self, i: int) -> int:
        return 2 * i + 1

    def _right_child(self, i: int) -> int:
        return 2 * i + 2

    def _is_higher_priority(self, a: WaitlistRequest, b: WaitlistRequest) -> bool:
        if a.priority != b.priority:
            return a.priority < b.priority
        return a.timestamp < b.timestamp

    def push(self, item: WaitlistRequest) -> None:
        """Insert element and sift-up in O(log N) time."""
        self.heap.append(item)
        i = len(self.heap) - 1
        while i > 0 and self._is_higher_priority(self.heap[i], self.heap[self._parent(i)]):
            parent_idx = self._parent(i)
            self.heap[i], self.heap[parent_idx] = self.heap[parent_idx], self.heap[i]
            i = parent_idx

    def pop(self) -> Optional[WaitlistRequest]:
        """Extract highest-priority element and sift-down in O(log N) time."""
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return root

    def _sift_down(self, i: int) -> None:
        size = len(self.heap)
        while True:
            smallest = i
            left = self._left_child(i)
            right = self._right_child(i)

            if left < size and self._is_higher_priority(self.heap[left], self.heap[smallest]):
                smallest = left
            if right < size and self._is_higher_priority(self.heap[right], self.heap[smallest]):
                smallest = right

            if smallest != i:
                self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
                i = smallest
            else:
                break

    def peek(self) -> Optional[WaitlistRequest]:
        return self.heap[0] if self.heap else None
