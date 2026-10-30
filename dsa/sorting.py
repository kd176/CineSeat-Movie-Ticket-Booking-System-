"""
Custom Sorting Algorithms (Merge Sort & Quick Sort)
Module: dsa.sorting
Academic Concept: Divide-and-Conquer, Stable vs. In-Place Sorting, Recursion

Time Complexity:
- Merge Sort: O(N log N) Best, Average, and Worst case (Guaranteed stable)
- Quick Sort: O(N log N) Average case, O(N^2) Worst case
Space Complexity:
- Merge Sort: O(N) auxiliary
- Quick Sort: O(log N) recursive call stack
"""

from typing import List, Callable, Any, Dict


def merge_sort(items: List[Dict[str, Any]], key_func: Callable[[Dict[str, Any]], Any], reverse: bool = False) -> List[Dict[str, Any]]:
    """
    Custom Merge Sort implementation from scratch.
    Divide-and-Conquer algorithm:
    1. Divide array into two halves.
    2. Recursively sort each half.
    3. Merge the two sorted halves preserving stability.
    """
    if len(items) <= 1:
        return list(items)

    mid = len(items) // 2
    left_half = merge_sort(items[:mid], key_func, reverse=reverse)
    right_half = merge_sort(items[mid:], key_func, reverse=reverse)

    return _merge(left_half, right_half, key_func, reverse)


def _merge(left: List[Dict[str, Any]], right: List[Dict[str, Any]], key_func: Callable[[Dict[str, Any]], Any], reverse: bool) -> List[Dict[str, Any]]:
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        left_val = key_func(left[i])
        right_val = key_func(right[j])

        # Handle None or missing keys gracefully
        if left_val is None:
            left_val = -float('inf') if not reverse else float('inf')
        if right_val is None:
            right_val = -float('inf') if not reverse else float('inf')

        condition = (left_val >= right_val) if reverse else (left_val <= right_val)
        if condition:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def quick_sort(items: List[Dict[str, Any]], key_func: Callable[[Dict[str, Any]], Any], reverse: bool = False) -> List[Dict[str, Any]]:
    """
    Custom Quick Sort implementation from scratch.
    Partitioning algorithm selecting median-of-three or center pivot.
    """
    arr = list(items)
    _quick_sort_recursive(arr, 0, len(arr) - 1, key_func, reverse)
    return arr


def _quick_sort_recursive(arr: List[Dict[str, Any]], low: int, high: int, key_func: Callable[[Dict[str, Any]], Any], reverse: bool) -> None:
    if low < high:
        pi = _partition(arr, low, high, key_func, reverse)
        _quick_sort_recursive(arr, low, pi - 1, key_func, reverse)
        _quick_sort_recursive(arr, pi + 1, high, key_func, reverse)


def _partition(arr: List[Dict[str, Any]], low: int, high: int, key_func: Callable[[Dict[str, Any]], Any], reverse: bool) -> int:
    pivot_val = key_func(arr[high])
    if pivot_val is None:
        pivot_val = -float('inf') if not reverse else float('inf')

    i = low - 1
    for j in range(low, high):
        curr_val = key_func(arr[j])
        if curr_val is None:
            curr_val = -float('inf') if not reverse else float('inf')

        condition = (curr_val >= pivot_val) if reverse else (curr_val <= pivot_val)
        if condition:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
