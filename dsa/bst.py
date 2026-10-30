"""
Binary Search Tree (BST) for Movie Indexing & Range Queries
Module: dsa.bst
Academic Concept: Non-linear Hierarchical Data Structure, BST Properties, In-Order Traversal

Time Complexity:
- Insert: O(H) where H is tree height (O(log N) average, O(N) worst case)
- Search: O(H)
- In-Order Traversal (Sorted Output): O(N)
- Range Search: O(H + K) where K is number of matched elements
Space Complexity: O(N)
"""

from typing import List, Dict, Any, Optional


class BSTNode:
    def __init__(self, key: float, movie: Dict[str, Any]):
        self.key: float = key                      # E.g., Rating (8.5) or Price (250)
        self.movies: List[Dict[str, Any]] = [movie] # Handles duplicate keys
        self.left: Optional[BSTNode] = None
        self.right: Optional[BSTNode] = None


class MovieBST:
    """
    Binary Search Tree to index movies by a numerical attribute (e.g. Rating, Price, or Runtime).
    Supports sorted in-order extraction and efficient range filtering.
    """

    def __init__(self, key_name: str = "rating"):
        self.root: Optional[BSTNode] = None
        self.key_name: str = key_name
        self.node_count: int = 0

    def insert(self, key: float, movie: Dict[str, Any]) -> None:
        """Insert a movie into BST ordered by `key`. Average Time: O(log N)."""
        key = float(key)
        if self.root is None:
            self.root = BSTNode(key, movie)
            self.node_count += 1
            return

        curr = self.root
        while True:
            if abs(curr.key - key) < 1e-6:
                # Key already exists: append movie to duplicate bucket
                curr.movies.append(movie)
                return
            elif key < curr.key:
                if curr.left is None:
                    curr.left = BSTNode(key, movie)
                    self.node_count += 1
                    return
                curr = curr.left
            else:
                if curr.right is None:
                    curr.right = BSTNode(key, movie)
                    self.node_count += 1
                    return
                curr = curr.right

    def inorder_traversal(self, reverse: bool = False) -> List[Dict[str, Any]]:
        """
        Standard In-Order Traversal yields strictly sorted movies in O(N) time.
        reverse=True yields descending order (e.g. highest rated first).
        """
        results: List[Dict[str, Any]] = []

        def _traverse(node: Optional[BSTNode]) -> None:
            if not node:
                return
            first = node.right if reverse else node.left
            second = node.left if reverse else node.right

            _traverse(first)
            results.extend(node.movies)
            _traverse(second)

        _traverse(self.root)
        return results

    def range_search(self, min_val: float, max_val: float) -> List[Dict[str, Any]]:
        """
        Efficient Range Query: Finds all movies whose key is in [min_val, max_val].
        Prunes subtrees that fall outside the range for optimal performance.
        Time Complexity: O(log N + K).
        """
        results: List[Dict[str, Any]] = []

        def _search(node: Optional[BSTNode]) -> None:
            if not node:
                return
            # If current key > min_val, there might be matching elements in left subtree
            if node.key > min_val:
                _search(node.left)
            # If current key is in range [min_val, max_val], collect
            if min_val <= node.key <= max_val:
                results.extend(node.movies)
            # If current key < max_val, there might be matching elements in right subtree
            if node.key < max_val:
                _search(node.right)

        _search(self.root)
        return results

    def find_min(self) -> Optional[float]:
        """Find minimum key in O(H) time."""
        if not self.root:
            return None
        curr = self.root
        while curr.left:
            curr = curr.left
        return curr.key

    def find_max(self) -> Optional[float]:
        """Find maximum key in O(H) time."""
        if not self.root:
            return None
        curr = self.root
        while curr.right:
            curr = curr.right
        return curr.key
