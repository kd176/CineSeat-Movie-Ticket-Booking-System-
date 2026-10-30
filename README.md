# CineSeat — Movie Ticket Booking System (Python DSA Edition)

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![DSA Test Suite](https://img.shields.io/badge/Unit%20Tests-100%25%20Passing-brightgreen.svg)](tests/test_dsa.py)
[![Academic Evaluation](https://img.shields.io/badge/Faculty%20Evaluator-Mr.%20Vivek-orange.svg)](#)

* **Student Name:** Khushi
* **Registration Number:** 251302194
* **Faculty / Evaluator:** Mr. Vivek
* **Course:** Data Structures and Algorithms in Python (Compulsory Python Requirement)
* **Academic Guide & Demo Script:** [PYTHON_DSA_GUIDE.md](PYTHON_DSA_GUIDE.md)

---

## Overview

**CineSeat** is an end-to-end Movie Ticket Booking System built with Python to demonstrate core Data Structures and Algorithms (DSA) concepts. It features 56 seeded films with HD posters, 3 Delhi NCR multiplexes (Citylight, Aurora, Horizon), deterministic show experiences (2D, 3D RealD, 4K Laser, Dolby Atmos), dynamic 2D seat matrix allocation, adjacent recliner recommendation, promo discounts, simulated atomic checkout, digital admission receipts, and automated FIFO waitlist reallocation.

---

## Data Structures & Algorithms (DSA) Implementation

The project implements textbook-clean data structures and algorithms from scratch in the `dsa/` module:

| Component | File | Data Structure / Algorithm | Time Complexity | Academic Purpose |
|---|---|---|---|---|
| **Cinema Hall Layout** | `dsa/seat_matrix.py` | 2D Array Matrix (`SeatMatrix`) | $O(1)$ access | 8×5 Cinema Hall Grid (Rows A–D Classic, E–F Premium, G–H Recliner). Prevents duplicate seat claims. |
| **Adjacent Recliner Suggestion** | `dsa/seat_matrix.py` | Sliding Window Spatial Search | $O(R \times C)$ | Finds contiguous seats in high-demand tiers minimizing distance from center screen. |
| **Movie Search & Autocomplete** | `dsa/trie.py` | Prefix Tree (`MovieTrie`) | $O(L)$ query | Instant title prefix search and autocomplete across 56 films. |
| **Rating & Price Indexing** | `dsa/bst.py` | Binary Search Tree (`MovieBST`) | $O(\log N + K)$ range | Supports range filtering and in-order sorted extraction. |
| **Waiting List Management** | `dsa/waitlist_queue.py` | FIFO Doubly Linked List Queue | $O(1)$ enqueue/dequeue | First-come, first-served customer allocation for sold-out shows. |
| **VIP / Priority Allocation** | `dsa/waitlist_queue.py` | Min-Heap Priority Queue | $O(\log N)$ push/pop | Prioritizes VIP or promotional booking allocations. |
| **Cancellation & Rollback** | `dsa/cancellation_stack.py` | LIFO Stack (`BookingHistoryStack`) | $O(1)$ push/pop | Records audit history, supports rollbacks and ticket cancellations. |
| **Delhi NCR Theatres Routing** | `dsa/theatre_graph.py` | Weighted Graph & Dijkstra's Algorithm | $O((V + E) \log V)$ | Computes shortest road route from user location to nearest CineSeat multiplex. |
| **Catalogue Sorting** | `dsa/sorting.py` | Merge Sort & Quick Sort | $O(N \log N)$ | Custom divide-and-conquer sorting by Rating (Merge) and Price/Hype (Quick). |
| **Digital Ticket Verification** | `dsa/hash_table.py` | Custom Chained Hash Table | $O(1)$ average lookup | Instant ticket token verification via rolling polynomial hash. |

---

## Quick Start (How to Run)

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Run All DSA Unit Tests
```bash
python main.py --test
```
*Runs all 9 unit tests in `tests/test_dsa.py` to verify algorithms.*

### 3. Launch Web Application
```bash
python main.py
```
Open **`http://127.0.0.1:5000`** in your browser to view the cinema booking interface, live seat grid, and DSA inspector.

### 4. Launch Interactive Terminal (CLI Mode)
```bash
python main.py --cli
```
Run the interactive terminal app with ASCII cinema seat maps and DSA benchmark tools.

---

## Video Recording (7–9 Minute OBS Guide)

Follow the complete 12-point recording script detailed in **[PYTHON_DSA_GUIDE.md](PYTHON_DSA_GUIDE.md)**:
1. Cover & Student Credentials (Khushi, 251302194, Mr. Vivek)
2. 56-Movie Catalogue & Merge/Quick Sort
3. Movie Title Search via Trie
4. Show Experiences across 3 Delhi NCR Theatres
5. 2D Seat Matrix & Adjacent Recliner Suggestion
6. Cart, Promo Code (`MOVIENIGHT`) & Simulated Checkout
7. Ticket Pass & Printable Receipt
8. Order Cancellation & Automated FIFO Waitlist Reallocation
9. Theatre Graph & Dijkstra Route Calculation
10. Code Walkthrough (`dsa/seat_matrix.py`, `dsa/trie.py`, `dsa/bst.py`, etc.)

---
*Created for University Evaluation · Faculty: Mr. Vivek · Student: Khushi (251302194)*
