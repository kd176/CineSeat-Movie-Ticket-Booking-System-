"""
Core Cinema Engine integrating Data Structures & Algorithms
Module: engine.cinema_manager
"""

import json
import os
import time
from typing import Dict, List, Any, Optional

from dsa.seat_matrix import SeatMatrix
from dsa.trie import MovieTrie
from dsa.bst import MovieBST
from dsa.waitlist_queue import FIFOQueue, WaitlistRequest
from dsa.cancellation_stack import BookingHistoryStack, BookingAction
from dsa.theatre_graph import TheatreGraph
from dsa.sorting import merge_sort, quick_sort
from dsa.hash_table import CustomHashTable
from .models import User, Booking


class CinemaManager:
    _instance: Optional['CinemaManager'] = None

    @classmethod
    def get_instance(cls) -> 'CinemaManager':
        if cls._instance is None:
            cls._instance = CinemaManager()
        return cls._instance

    def __init__(self):
        self.theatres = [
            {
                "id": "citylight",
                "name": "CineSeat Citylight",
                "area": "Connaught Place",
                "city": "Delhi NCR",
                "address": "Plaza Cinema Complex, Connaught Place, New Delhi",
                "format": "2D",
                "projection": "HD / 2K Laser",
                "audio": "Dolby 7.1",
                "subtitles": "English",
                "premium": 0,
                "amenities": ["Parking", "Food court", "Wheelchair access"]
            },
            {
                "id": "aurora",
                "name": "CineSeat Aurora",
                "area": "Saket",
                "city": "Delhi NCR",
                "address": "Select Citywalk, Saket District Centre, New Delhi",
                "format": "2D",
                "projection": "4K Laser",
                "audio": "Dolby Atmos",
                "subtitles": "English",
                "premium": 60,
                "amenities": ["Valet Parking", "VIP Lounge", "Recliners", "Dolby Atmos"]
            },
            {
                "id": "horizon",
                "name": "CineSeat Horizon",
                "area": "Noida Sector 18",
                "city": "Delhi NCR",
                "address": "Great India Place Mall, Sector 38-A, Noida",
                "format": "3D",
                "projection": "4K Laser RealD 3D",
                "audio": "Dolby Atmos 64-Ch",
                "subtitles": "None",
                "premium": 100,
                "amenities": ["Parking", "Gourmet Diner", "Recliners", "RealD 3D"]
            }
        ]
        self.performance_times = ["10:00", "14:00", "18:00", "22:00"]

        # Data structures
        self.trie = MovieTrie()
        self.rating_bst = MovieBST(key_name="rating")
        self.price_bst = MovieBST(key_name="price")
        self.theatre_graph = TheatreGraph()
        self.history_stack = BookingHistoryStack()
        self.ticket_table = CustomHashTable()

        # Performance-keyed structures
        self.seat_matrices: Dict[str, SeatMatrix] = {}
        self.waitlist_queues: Dict[str, FIFOQueue] = {}

        # Master movie collections
        self.movies: List[Dict[str, Any]] = []
        self.movies_by_id: Dict[int, Dict[str, Any]] = {}
        self.releases: List[Dict[str, Any]] = []

        # In-memory storage for bookings and orders
        self.bookings: List[Booking] = []
        self.next_order_id = 10001
        self.next_booking_id = 50001
        self.next_waitlist_id = 1

        self._load_data()

    def _load_data(self) -> None:
        """Load seeded catalogue, enrichment, and release announcements."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cat_path = os.path.join(base_dir, "server", "catalogue.json")
        enr_path = os.path.join(base_dir, "server", "enrichment.json")
        rel_path = os.path.join(base_dir, "server", "releases.json")

        catalogue = []
        enrichment = {}
        if os.path.exists(cat_path):
            with open(cat_path, "r", encoding="utf-8") as f:
                catalogue = json.load(f)
        if os.path.exists(enr_path):
            with open(enr_path, "r", encoding="utf-8") as f:
                enrichment = json.load(f)
        if os.path.exists(rel_path):
            with open(rel_path, "r", encoding="utf-8") as f:
                self.releases = json.load(f)

        for m in catalogue:
            mid = m["id"]
            enr = enrichment.get(str(mid), {})
            
            # Combine catalogue with enrichment details
            full_movie = {
                "id": mid,
                "name": m.get("name", "Untitled"),
                "genre": m.get("genre", "General"),
                "duration": m.get("duration", 120),
                "price": m.get("price", 250),
                "tag": m.get("tag", "NOW SHOWING"),
                "synopsis": m.get("synopsis", "Experience on the big screen with premium sound."),
                "language": m.get("language", "Hindi"),
                "rating": enr.get("rating", round(7.0 + (mid % 27) * 0.1, 1)),
                "year": enr.get("year", 2024),
                "director": enr.get("director", "Acclaimed Filmmaker"),
                "cast": enr.get("cast", "Star Cast"),
                "poster": f"/posters/{mid}.jpg" if os.path.exists(os.path.join(base_dir, "public", "posters", f"{mid}.jpg")) else m.get("art"),
                "trailerUrl": enr.get("trailerUrl") or enr.get("teaserUrl") or "https://www.youtube.com",
                "hypeScore": (mid * 37) % 500 + 150
            }

            self.movies.append(full_movie)
            self.movies_by_id[mid] = full_movie

            # Index into DSA structures
            self.trie.insert(full_movie["name"], full_movie)
            self.rating_bst.insert(full_movie["rating"], full_movie)
            self.price_bst.insert(full_movie["price"], full_movie)

    def search_movies(self, query: str) -> List[Dict[str, Any]]:
        """Search movies using Prefix Trie in O(P + K) time."""
        if not query or not query.strip():
            return self.movies
        return self.trie.search_prefix(query)

    def get_sorted_movies(self, sort_by: str = "rating", reverse: bool = True) -> List[Dict[str, Any]]:
        """
        Sort movies using custom Divide-and-Conquer Sorting Algorithms:
        - 'rating': Merge Sort (O(N log N))
        - 'price': Quick Sort (O(N log N))
        - 'name': Merge Sort (O(N log N))
        - 'hype': Quick Sort (O(N log N))
        """
        if sort_by == "rating":
            return merge_sort(self.movies, key_func=lambda m: m.get("rating", 0), reverse=reverse)
        elif sort_by == "price":
            return quick_sort(self.movies, key_func=lambda m: m.get("price", 0), reverse=reverse)
        elif sort_by == "name":
            return merge_sort(self.movies, key_func=lambda m: m.get("name", "").lower(), reverse=reverse)
        elif sort_by == "hype":
            return quick_sort(self.movies, key_func=lambda m: m.get("hypeScore", 0), reverse=reverse)
        return self.movies

    def filter_by_rating_range(self, min_rating: float, max_rating: float) -> List[Dict[str, Any]]:
        """Query movies in rating range [min_rating, max_rating] using MovieBST."""
        return self.rating_bst.range_search(min_rating, max_rating)

    def get_or_create_seat_matrix(self, show_key: str, base_price: int = 250) -> SeatMatrix:
        """Fetch or instantiate 2D Seat Matrix for a performance."""
        if show_key not in self.seat_matrices:
            self.seat_matrices[show_key] = SeatMatrix(rows=8, cols=5, base_price=base_price)
        return self.seat_matrices[show_key]

    def get_or_create_waitlist_queue(self, show_key: str) -> FIFOQueue:
        """Fetch or instantiate FIFO Waiting List Queue for a performance."""
        if show_key not in self.waitlist_queues:
            self.waitlist_queues[show_key] = FIFOQueue()
        return self.waitlist_queues[show_key]

    def get_performances(self, movie_id: int, date: str) -> List[Dict[str, Any]]:
        """Generate deterministic show experiences across all 3 Delhi NCR theatres."""
        movie = self.movies_by_id.get(movie_id)
        if not movie:
            return []

        shows = []
        for index, venue in enumerate(self.theatres):
            time_slot = self.performance_times[(movie_id - 1 + index) % 4]
            is_3d = venue["format"] == "3D" and any(g in movie["genre"] for g in ["Animation", "Sci-Fi", "Adventure", "Action"])
            fmt = "3D" if is_3d else "2D"
            venue_premium = venue["premium"]
            base_price = movie["price"] + venue_premium
            
            show_key = f"{movie_id}|{date}|{time_slot}|{venue['id']}"
            matrix = self.get_or_create_seat_matrix(show_key, base_price=base_price)
            queue = self.get_or_create_waitlist_queue(show_key)

            shows.append({
                "id": show_key,
                "movieId": movie_id,
                "movieTitle": movie["name"],
                "date": date,
                "time": time_slot,
                "theatreId": venue["id"],
                "theatreName": venue["name"],
                "area": venue["area"],
                "address": venue["address"],
                "screen": f"Screen {(movie_id % 3) + 1}",
                "format": fmt,
                "projection": venue["projection"],
                "audio": venue["audio"],
                "subtitles": venue["subtitles"],
                "basePrice": base_price,
                "capacity": 40,
                "availableSeats": matrix.get_available_seats_count(),
                "waitlistCount": queue.size(),
                "amenities": venue["amenities"]
            })
        return shows

    def suggest_adjacent_seats(self, show_key: str, count: int = 2, tier: str = "Recliner") -> List[str]:
        """Adjacent seat suggestion algorithm via SeatMatrix."""
        matrix = self.get_or_create_seat_matrix(show_key)
        return matrix.suggest_best_adjacent_seats(count=count, preferred_tier=tier)

    def create_booking_order(
        self,
        user: User,
        items: List[Dict[str, Any]],
        snacks_count: int = 0,
        promo_code: str = "",
        payment_mode: str = "UPI"
    ) -> Dict[str, Any]:
        """
        Atomic checkout transaction for 1 to 8 shows in one order:
        - Validates seat availability in each SeatMatrix.
        - Reserves seats atomically.
        - Applies snacks and promo code discounts.
        - Generates tickets and indexes into CustomHashTable.
        - Pushes order creation snapshot to BookingHistoryStack.
        """
        if not items:
            raise ValueError("No items in order.")

        order_id = self.next_order_id
        self.next_order_id += 1

        subtotal = 0.0
        allocated_bookings: List[Booking] = []
        rollback_actions = []

        try:
            for item in items:
                show_key = item["showKey"]
                seat_labels = item["seats"]
                matrix = self.get_or_create_seat_matrix(show_key)

                # Verify and book seats atomically
                booking_id = self.next_booking_id
                self.next_booking_id += 1

                success = matrix.book_seats(seat_labels, user_id=user.email, booking_id=booking_id)
                if not success:
                    raise ValueError(f"One or more selected seats in show {show_key} are already booked.")

                rollback_actions.append((matrix, seat_labels))

                # Calculate item total
                item_total = sum(matrix.get_seat(lbl).price for lbl in seat_labels)
                subtotal += item_total

                # Parse show details
                parts = show_key.split("|")
                mid = int(parts[0])
                date = parts[1]
                time_slot = parts[2]
                theatre_id = parts[3]
                theatre = next((t for t in self.theatres if t["id"] == theatre_id), self.theatres[0])
                movie = self.movies_by_id.get(mid, {"name": "Movie"})

                booking = Booking(
                    booking_id=booking_id,
                    order_id=order_id,
                    user_id=user.user_id,
                    user_name=user.name,
                    movie_id=mid,
                    movie_title=movie["name"],
                    show_key=show_key,
                    theatre_id=theatre_id,
                    theatre_name=theatre["name"],
                    date=date,
                    time_slot=time_slot,
                    screen=f"Screen {(mid % 3) + 1}",
                    format_type=theatre["format"],
                    seats=seat_labels,
                    total_amount=item_total,
                    payment_mode=payment_mode
                )
                allocated_bookings.append(booking)
                self.bookings.append(booking)

                # Store in custom hash table for O(1) ticket lookups
                ticket_key = f"TICKET-{booking_id}"
                self.ticket_table.insert(ticket_key, booking.to_dict())

            # Apply promo code discount (10% off with MOVIENIGHT)
            discount = 0.0
            if promo_code.strip().upper() == "MOVIENIGHT":
                discount = round(subtotal * 0.10, 2)

            snack_cost = snacks_count * 180.0
            grand_total = subtotal - discount + snack_cost

            # Record action in History Stack (for audit & rollback)
            action = BookingAction(
                action_type="ORDER_CREATED",
                order_id=order_id,
                user_id=user.user_id,
                snapshot={
                    "orderId": order_id,
                    "grandTotal": grand_total,
                    "bookingIds": [b.booking_id for b in allocated_bookings]
                }
            )
            self.history_stack.push(action)

            return {
                "orderId": order_id,
                "subtotal": subtotal,
                "discount": discount,
                "snacks": snacks_count,
                "snackCost": snack_cost,
                "grandTotal": grand_total,
                "mode": payment_mode,
                "status": "Confirmed",
                "bookings": [b.to_dict() for b in allocated_bookings]
            }

        except Exception as e:
            # Transaction rollback: release any seats booked in this failed order
            for matrix, labels in rollback_actions:
                matrix.release_seats(labels)
            raise e

    def cancel_booking(self, booking_id: int, user_id: str) -> Dict[str, Any]:
        """
        Cancel a booking:
        1. Locate booking and update status.
        2. Release seats in the respective SeatMatrix.
        3. Push cancellation event to BookingHistoryStack (LIFO).
        4. Reallocate freed seats to earliest group waiting in FIFOQueue!
        """
        booking = next((b for b in self.bookings if b.booking_id == booking_id), None)
        if not booking:
            raise ValueError("Booking not found.")

        if booking.status == "Cancelled":
            return {"status": "Already Cancelled", "bookingId": booking_id}

        # Release seats in 2D Matrix
        matrix = self.get_or_create_seat_matrix(booking.show_key)
        matrix.release_seats(booking.seats)
        booking.status = "Cancelled"

        # Push to LIFO History Stack
        action = BookingAction(
            action_type="BOOKING_CANCELLED",
            order_id=booking.order_id,
            user_id=user_id,
            snapshot={"bookingId": booking_id, "freedSeats": booking.seats, "showKey": booking.show_key}
        )
        self.history_stack.push(action)

        # Update Ticket Hash Table
        self.ticket_table.insert(f"TICKET-{booking_id}", booking.to_dict())

        # Automatic FIFO Waitlist Allocation
        waitlist_reallocated = self._attempt_waitlist_allocation(booking.show_key)

        return {
            "success": True,
            "bookingId": booking_id,
            "status": "Cancelled",
            "refundAmount": booking.total_amount,
            "waitlistReallocated": waitlist_reallocated
        }

    def _attempt_waitlist_allocation(self, show_key: str) -> Optional[Dict[str, Any]]:
        """
        Inspect FIFO Queue for the show. If the head waiting customer's requested
        seat count can be fulfilled by currently available seats, allocate them immediately!
        """
        queue = self.get_or_create_waitlist_queue(show_key)
        if queue.is_empty():
            return None

        matrix = self.get_or_create_seat_matrix(show_key)
        available_count = matrix.get_available_seats_count()

        head_req = queue.peek()
        if head_req and available_count >= head_req.seat_count:
            # Dequeue customer
            req = queue.dequeue()
            # Suggest best available seats for waitlisted group
            allocated_seats = matrix.suggest_best_adjacent_seats(count=req.seat_count)
            if not allocated_seats:
                # Fallback: grab any available seats
                allocated_seats = []
                for r in range(matrix.num_rows):
                    for c in range(matrix.num_cols):
                        if matrix.grid[r][c].status == "Available" and len(allocated_seats) < req.seat_count:
                            allocated_seats.append(matrix.grid[r][c].label)

            booking_id = self.next_booking_id
            self.next_booking_id += 1
            matrix.book_seats(allocated_seats, user_id=req.user_id, booking_id=booking_id)

            parts = show_key.split("|")
            mid = int(parts[0])
            theatre_id = parts[3]
            theatre = next((t for t in self.theatres if t["id"] == theatre_id), self.theatres[0])
            movie = self.movies_by_id.get(mid, {"name": "Movie"})

            waitlist_booking = Booking(
                booking_id=booking_id,
                order_id=self.next_order_id,
                user_id=req.user_id,
                user_name=req.user_name,
                movie_id=mid,
                movie_title=movie["name"],
                show_key=show_key,
                theatre_id=theatre_id,
                theatre_name=theatre["name"],
                date=parts[1],
                time_slot=parts[2],
                screen=f"Screen {(mid % 3) + 1}",
                format_type=theatre["format"],
                seats=allocated_seats,
                total_amount=sum(matrix.get_seat(s).price for s in allocated_seats),
                payment_mode="Pay at Counter"
            )
            self.bookings.append(waitlist_booking)
            self.ticket_table.insert(f"TICKET-{booking_id}", waitlist_booking.to_dict())

            return {
                "allocated": True,
                "user": req.user_name,
                "seats": allocated_seats,
                "bookingId": booking_id
            }
        return None

    def join_waitlist(self, user: User, show_key: str, seat_count: int) -> Dict[str, Any]:
        """Add user to FIFO Waiting List for a sold-out or busy show."""
        queue = self.get_or_create_waitlist_queue(show_key)
        req_id = self.next_waitlist_id
        self.next_waitlist_id += 1

        req = WaitlistRequest(
            request_id=req_id,
            user_id=user.user_id,
            user_name=user.name,
            show_key=show_key,
            seat_count=seat_count
        )
        queue.enqueue(req)
        return {
            "success": True,
            "requestId": req_id,
            "position": queue.size(),
            "showKey": show_key,
            "seatCount": seat_count
        }

    def get_user_bookings(self, user_id: str) -> List[Dict[str, Any]]:
        """Retrieve booking history for a user."""
        return [b.to_dict() for b in reversed(self.bookings) if b.user_id == user_id]

    def verify_ticket(self, ticket_code: str) -> Optional[Dict[str, Any]]:
        """Instant O(1) ticket verification via CustomHashTable."""
        return self.ticket_table.get(ticket_code.strip().upper())

    def get_dsa_diagnostics(self) -> Dict[str, Any]:
        """
        Diagnostic summary of all active DSA structures for presentation & viva.
        """
        return {
            "movieTrie": {
                "totalIndexedWords": self.trie.total_words,
                "rootChildBranches": len(self.trie.root.children),
                "lookupComplexity": "O(L) - Length of query prefix"
            },
            "ratingBST": {
                "totalNodes": self.rating_bst.node_count,
                "minRating": self.rating_bst.find_min(),
                "maxRating": self.rating_bst.find_max(),
                "rangeQueryComplexity": "O(log N + K)"
            },
            "seatMatricesActive": len(self.seat_matrices),
            "theatreGraph": {
                "totalHubs": len(self.theatre_graph.adj),
                "venuesConnected": len(self.theatre_graph.venues),
                "algorithm": "Dijkstra's Shortest Path - O((V + E) log V)"
            },
            "historyStackSize": self.history_stack.size(),
            "ticketHashTable": {
                "capacity": self.ticket_table.capacity,
                "storedTickets": self.ticket_table.size,
                "loadFactor": round(self.ticket_table.size / self.ticket_table.capacity, 3),
                "lookupComplexity": "O(1) Average"
            }
        }
