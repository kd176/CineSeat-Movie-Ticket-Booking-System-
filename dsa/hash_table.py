"""
Custom Hash Table with Separate Chaining
Module: dsa.hash_table
Academic Concept: Hash Function, Collision Resolution (Chaining), Dynamic Load Factor

Time Complexity:
- Insert: O(1) average, O(N) worst case (if all keys collide)
- Lookup: O(1) average, O(N) worst case
- Delete: O(1) average, O(N) worst case
Space Complexity: O(M + N) where M is bucket count and N is stored items
"""

from typing import Any, Optional, List, Tuple


class HashNode:
    def __init__(self, key: str, value: Any):
        self.key: str = key
        self.value: Any = value
        self.next: Optional['HashNode'] = None


class CustomHashTable:
    """
    Hash Table implemented from scratch with separate chaining.
    Used for instant O(1) digital ticket verification and fast user lookups.
    """

    def __init__(self, initial_capacity: int = 37):
        self.capacity: int = initial_capacity
        self.size: int = 0
        self.buckets: List[Optional[HashNode]] = [None] * self.capacity
        self.load_factor_threshold: float = 0.75

    def _hash(self, key: str) -> int:
        """
        Polynomial rolling hash function:
        hash = (sum(c * 31^i)) mod capacity
        """
        hash_val = 0
        prime_multiplier = 31
        for char in str(key):
            hash_val = (hash_val * prime_multiplier + ord(char)) % self.capacity
        return hash_val

    def insert(self, key: str, value: Any) -> None:
        """Insert or update key-value pair in O(1) average time."""
        index = self._hash(key)
        head = self.buckets[index]

        # Check if key already exists in bucket chain
        curr = head
        while curr:
            if curr.key == key:
                curr.value = value
                return
            curr = curr.next

        # Key not present, insert at head of chain
        new_node = HashNode(key, value)
        new_node.next = self.buckets[index]
        self.buckets[index] = new_node
        self.size += 1

        # Resize if load factor exceeds threshold
        if (self.size / self.capacity) > self.load_factor_threshold:
            self._resize()

    def get(self, key: str) -> Optional[Any]:
        """Retrieve value by key in O(1) average time."""
        index = self._hash(key)
        curr = self.buckets[index]
        while curr:
            if curr.key == key:
                return curr.value
            curr = curr.next
        return None

    def contains(self, key: str) -> bool:
        return self.get(key) is not None

    def delete(self, key: str) -> bool:
        """Delete key from hash table in O(1) average time."""
        index = self._hash(key)
        curr = self.buckets[index]
        prev: Optional[HashNode] = None

        while curr:
            if curr.key == key:
                if prev:
                    prev.next = curr.next
                else:
                    self.buckets[index] = curr.next
                self.size -= 1
                return True
            prev = curr
            curr = curr.next
        return False

    def _resize(self) -> None:
        """Double capacity and rehash all nodes."""
        old_buckets = self.buckets
        self.capacity = self.capacity * 2 + 1
        self.buckets = [None] * self.capacity
        self.size = 0

        for head in old_buckets:
            curr = head
            while curr:
                self.insert(curr.key, curr.value)
                curr = curr.next
