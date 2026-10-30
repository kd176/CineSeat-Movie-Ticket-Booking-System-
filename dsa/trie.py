"""
Trie (Prefix Tree) for Movie Title Search & Autocomplete
Module: dsa.trie
Academic Concept: Trie Data Structure, Prefix Matching, String Indexing

Time Complexity:
- Insert: O(L) where L is string length
- Search Prefix: O(P + K) where P is prefix length and K is the number of matching items
- Autocomplete: O(P + K)
Space Complexity: O(Total characters in all titles * Alphabet size)
"""

from typing import Dict, List, Any, Optional, Set


class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_end_of_word: bool = False
        # Store references to movie dictionaries matching this prefix/word
        self.movies: List[Dict[str, Any]] = []


class MovieTrie:
    """
    Prefix Tree (Trie) enabling sub-millisecond autocomplete and prefix search
    over all movie titles in the CineSeat catalogue.
    """

    def __init__(self):
        self.root = TrieNode()
        self.total_words = 0

    def insert(self, title: str, movie: Dict[str, Any]) -> None:
        """
        Insert full title and each individual word into the Trie.
        Example: "Spider-Man: Across the Spider-Verse" indexes:
        - "spider-man"
        - "across"
        - "spider-verse"
        - full normalized title
        """
        if not title:
            return

        normalized_full = title.strip().lower()
        self._insert_string(normalized_full, movie)

        # Also index individual tokens (words) for flexible keyword search
        words = [w for w in normalized_full.replace('-', ' ').replace(':', ' ').split() if len(w) > 1]
        for word in words:
            self._insert_string(word, movie)
        
        self.total_words += 1

    def _insert_string(self, text: str, movie: Dict[str, Any]) -> None:
        node = self.root
        for char in text:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            # Avoid duplicate movie entries in the same node
            if not any(m.get("id") == movie.get("id") for m in node.movies):
                node.movies.append(movie)
        node.is_end_of_word = True

    def search_prefix(self, prefix: str) -> List[Dict[str, Any]]:
        """
        Return all unique movies whose title or any token starts with `prefix`.
        Time Complexity: O(P) to locate node, then O(K) where K is matching movies.
        """
        if not prefix:
            return []

        prefix = prefix.strip().lower()
        node = self.root

        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        # Deduplicate results by movie ID
        seen_ids: Set[int] = set()
        unique_results: List[Dict[str, Any]] = []
        for movie in node.movies:
            mid = movie.get("id")
            if mid not in seen_ids:
                seen_ids.add(mid)
                unique_results.append(movie)

        return unique_results

    def autocomplete(self, prefix: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Return top `limit` movie suggestions for dynamic search bar."""
        results = self.search_prefix(prefix)
        return results[:limit]
