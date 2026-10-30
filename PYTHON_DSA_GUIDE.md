# CineSeat — Python DSA Movie Ticket Booking System
**Comprehensive Academic Submission & Evaluation Guide**

* **Student Name:** Khushi
* **Registration Number:** 251302194
* **Faculty / Evaluator:** Mr. Vivek
* **Course:** Data Structures and Algorithms in Python
* **Language & Runtime:** Python 3.14 / 3.x
* **Repository:** [https://github.com/kd176/CineSeat-Movie-Ticket-Booking-System-](https://github.com/kd176/CineSeat-Movie-Ticket-Booking-System-)

---

## 1. Executive Summary & Problem Statement

Commercial cinema reservation platforms face strict data integrity constraints: simultaneous seat reservations, fair queuing for sold-out shows, sub-millisecond title lookups, spatial seat recommendations, and distance-based multiplex routing.

**CineSeat** implements a full-featured, production-grade Movie Ticket Booking System built entirely upon foundational **Data Structures and Algorithms (DSA) in Python**. The application includes 56 seeded films, three Delhi NCR cinema multiplexes, deterministic show schedules, interactive seating grids (Classic, Premium, Recliner), atomic checkout, promo discount computation, digital admission pass generation, and automated waitlist reallocation.

---

## 2. Core Data Structures & Algorithmic Complexity

| # | Academic Concept | File Path | Class / Algorithm | Time Complexity | Space Complexity | Real-World Application |
|---|---|---|---|---|---|---|
| **1** | **2D Matrix / Grid** | `dsa/seat_matrix.py` | `SeatMatrix`, `Seat` | **O(1)** access/booking | **O(R × C)** | 8×5 Hall layout (Rows A–D Classic, E–F Premium, G–H Recliner). Prevents duplicate seat claims. |
| **2** | **Sliding Window Spatial Search** | `dsa/seat_matrix.py` | `suggest_best_adjacent_seats` | **O(R × C)** | **O(K)** | Automatically finds $K$ adjacent empty Recliner seats with minimal distance from central screen angle. |
| **3** | **Prefix Tree (Trie)** | `dsa/trie.py` | `MovieTrie`, `TrieNode` | **O(L)** lookup ($L$ = query len) | **O(N × L)** | Instant autocomplete and multi-word title prefix search across 56 catalogue films. |
| **4** | **Binary Search Tree (BST)** | `dsa/bst.py` | `MovieBST`, `BSTNode` | **O(log N)** search, **O(log N + K)** range | **O(N)** | Indexes movies by rating (1.0–10.0) and price; enables range queries and in-order sorted traversal. |
| **5** | **FIFO Doubly Linked List Queue** | `dsa/waitlist_queue.py` | `FIFOQueue`, `Node` | **O(1)** enqueue/dequeue | **O(N)** | Enforces strict first-come, first-served customer waitlists for sold-out performances without head-of-line skipping. |
| **6** | **Min-Heap Priority Queue** | `dsa/waitlist_queue.py` | `PriorityWaitlist` | **O(log N)** push/pop | **O(N)** | Allocates limited promotional/VIP seats based on priority tier and timestamp. |
| **7** | **LIFO Stack** | `dsa/cancellation_stack.py` | `BookingHistoryStack` | **O(1)** push/pop/peek | **O(N)** | Transaction rollback log and order cancellation history for undo operations. |
| **8** | **Weighted Graph & Dijkstra's Algorithm** | `dsa/theatre_graph.py` | `TheatreGraph`, `dijkstra_shortest_path` | **O((V + E) log V)** | **O(V + E)** | Models Delhi NCR road network and computes shortest driving distance from user location to CineSeat multiplexes. |
| **9** | **Custom Merge Sort & Quick Sort** | `dsa/sorting.py` | `merge_sort`, `quick_sort` | **O(N log N)** | **O(N)** / **O(log N)** | Sorts catalogue by Rating (Merge Sort - stable) and Price/Hype Score (Quick Sort - in-place). |
| **10** | **Custom Hash Table** | `dsa/hash_table.py` | `CustomHashTable`, chaining | **O(1)** average lookup/insert | **O(M + N)** | Instant digital ticket verification and order lookup using rolling polynomial hash with prime modulus. |

---

## 3. How to Run & Verify

### Step 1: Install Dependencies
Open PowerShell or Terminal inside the project root:
```bash
pip install -r requirements.txt
```
*(Only lightweight packages: `Flask` and `flask-cors`)*

### Step 2: Run Unit Tests (100% Pass Rate)
Verify all 9 DSA algorithms and data structures:
```bash
python main.py --test
```
*Expected output: `Ran 9 tests in 0.002s. OK`*

### Step 3: Run Interactive Terminal CLI Mode
Experience the complete text-based booking system with ASCII seat maps:
```bash
python main.py --cli
# or
python cli.py
```

### Step 4: Run Modern Web Application
Start the full web interface:
```bash
python main.py
# or
python app.py
```
Open your browser at: **`http://127.0.0.1:5000`**

---

## 4. Suggested 7–9 Minute OBS Demo Video Script (For Khushi)

Set up OBS Studio (Display Capture, 1920×1080, 30 FPS, Mic muted or voiceover optional). Follow this exact sequence:

1. **Cover & Academic Introduction (0:00 – 0:45)**
   - Show top academic credentials bar on screen:
     - Project: CineSeat Movie Ticket Booking System
     - Student: Khushi (Reg No: 251302194)
     - Faculty Evaluator: Mr. Vivek
     - Subject: Data Structures and Algorithms in Python
2. **Movie Catalogue & Custom Sorting (0:45 – 1:45)**
   - Point out 56 films seeded with HD posters, metadata, genre, and duration.
   - Switch sort dropdown:
     - Top Rated (demonstrating **Merge Sort - O(N log N)**).
     - Price: Low to High (demonstrating **Quick Sort - O(N log N)**).
     - Popularity Hype.
3. **Movie Title Search via Trie (1:45 – 2:30)**
   - Type `"path"` in the search bar — instant match for *Pathaan*.
   - Type `"doom"` — prefix match for *Avengers: Doomsday*.
   - Explain how **MovieTrie** provides $O(L)$ time complexity instead of scanning all 56 films.
4. **Show Experiences across 3 Delhi NCR Multiplexes (2:30 – 3:30)**
   - Click "Book Tickets" on *Pathaan*.
   - Show the 3 venues:
     - *CineSeat Citylight* (Connaught Place) — 2D HD/2K
     - *CineSeat Aurora* (Saket) — 4K Laser, Dolby Atmos (+₹60)
     - *CineSeat Horizon* (Noida Sector 18) — 3D RealD (+₹100)
5. **2D Seat Matrix & Adjacent Recliner Suggestion (3:30 – 4:45)**
   - Highlight the 8×5 Cinema Hall layout: Rows A–D Classic (₹250), Rows E–F Premium (₹310), Rows G–H Recliner (₹450).
   - Click **"Suggest 2 Recliners (Sliding Window)"**.
   - Show seats `H2` and `H3` automatically selected. Explain the sliding window algorithm minimizing distance from the center viewing angle.
6. **Cart, Promo Discount & Simulated Checkout (4:45 – 5:45)**
   - Add 1 Snacks Combo (+₹180).
   - Enter promo code `MOVIENIGHT` (10% discount applied).
   - Select UPI / Card / Cash and click "Confirm & Generate Ticket".
   - Show digital admission pass modal with unique Ticket ID (`TICKET-50001`), barcode representation, and print option.
7. **Cancellation & Automated FIFO Waitlist Allocation (5:45 – 6:45)**
   - Go to "🎟️ My Tickets".
   - Click "Cancel Ticket".
   - Explain how this pushes an audit record to the **BookingHistoryStack (LIFO)**, frees the seats in the **SeatMatrix**, and checks the **FIFO Queue** to automatically reallocate the released seats to the next waiting customer.
8. **Delhi NCR Theatres Route Finder with Dijkstra's Algorithm (6:45 – 7:30)**
   - Switch to "📍 NCR Theatres (Dijkstra)".
   - Change starting location to *Karol Bagh* or *Nehru Place*.
   - Show shortest path calculation: `Karol Bagh -> Connaught Place` (4.2 km, 10 mins).
9. **Code Walkthrough & DSA Inspector Tab (7:30 – 8:30)**
   - Switch to "⚡ DSA Architecture & Live Inspector" tab on the web app.
   - Open VS Code to briefly show:
     - `dsa/seat_matrix.py` (2D Grid & recommendation algorithm)
     - `dsa/trie.py` (Prefix tree nodes & autocomplete)
     - `dsa/bst.py` (Binary Search Tree in-order traversal)
     - `dsa/waitlist_queue.py` (Doubly linked list FIFO Queue)
     - `dsa/theatre_graph.py` (Dijkstra shortest path algorithm)
   - Conclude recording showing clean project exit.

---

## 5. Faculty Viva Questions & Answers (Mr. Vivek)

**Q1: Why did you choose a Trie for movie search instead of a Hash Map or regular string search?**
> *Answer:* A standard Hash Map only supports exact key lookups $O(1)$. For prefix search (e.g. typing `"pat"` to find `"Pathaan"`), a Hash Map requires scanning every key, yielding $O(N \times M)$ time complexity. A Trie allows prefix searching in $O(L)$ time, where $L$ is the length of the query string, completely independent of the number of movies in the database.

**Q2: How does your adjacent seat recommendation algorithm work?**
> *Answer:* It models the hall as a 2D matrix ($R \times C$). It uses a sliding window of size $K$ across each row in the desired tier (Recliner rows G and H). For every valid contiguous window of available seats, it computes a spatial penalty based on Euclidean distance from the central column $((C - 1) / 2)$ and vertical row viewing depth. The window with the minimal penalty is returned.

**Q3: How is fairness guaranteed in the waiting list?**
> *Answer:* We implemented a Doubly Linked List FIFO Queue (`FIFOQueue`). Customers join at the tail in $O(1)$ time and are dequeued from the head in $O(1)$ time. When a booking cancellation occurs, the system inspects the head. If the head customer's requested seat count $\le$ currently available seats, they are allocated without allowing smaller, later groups to jump the queue.

**Q4: Why use Dijkstra's Algorithm for theatre selection?**
> *Answer:* Cinema customers in Delhi NCR travel from various sectors and hubs. By representing urban hubs and multiplex locations as a weighted undirected graph with road distances as weights, Dijkstra's Algorithm finds the optimal driving route and minimal distance in $O((V + E) \log V)$ time using a binary min-heap.

---
*Created for Academic Submission · Khushi (251302194) · Evaluator: Mr. Vivek*
