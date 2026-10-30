"""
CineSeat - Data Structures & Algorithms (DSA) Package
Author: Khushi (Registration No. 251302194)
Course: Data Structures and Algorithms in Python
Teacher / Evaluator: Mr. Vivek
Project: CineSeat Movie Ticket Booking System

This package provides custom-built data structures and algorithmic routines:
- SeatMatrix: 2D Matrix for hall seating, state tracking & adjacent seat recommendation.
- MovieTrie: Prefix Tree for fast O(L) title lookup and autocomplete.
- MovieBST: Binary Search Tree for rating/price indexing and range queries.
- FIFOQueue & PriorityWaitlist: Queues for waiting list allocation on sold-out shows.
- BookingHistoryStack: LIFO Stack for order rollback, cancellation history, and undo.
- TheatreGraph: Graph with Dijkstra's algorithm for shortest-distance theatre routing.
- MergeSort & QuickSort: Custom divide-and-conquer sorting algorithms for movies.
- CustomHashTable: Chained hash table for O(1) ticket verification.
"""

from .seat_matrix import SeatMatrix, SeatTier
from .trie import MovieTrie
from .bst import MovieBST
from .waitlist_queue import FIFOQueue, PriorityWaitlist, WaitlistRequest
from .cancellation_stack import BookingHistoryStack, BookingAction
from .theatre_graph import TheatreGraph
from .sorting import merge_sort, quick_sort
from .hash_table import CustomHashTable

__all__ = [
    "SeatMatrix",
    "SeatTier",
    "MovieTrie",
    "MovieBST",
    "FIFOQueue",
    "PriorityWaitlist",
    "WaitlistRequest",
    "BookingHistoryStack",
    "BookingAction",
    "TheatreGraph",
    "merge_sort",
    "quick_sort",
    "CustomHashTable",
]
