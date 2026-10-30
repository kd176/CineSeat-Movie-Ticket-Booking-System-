"""
Unit Test Suite for CineSeat DSA Package
Student: Khushi (Registration No. 251302194)
Course: Data Structures and Algorithms in Python
Teacher / Evaluator: Mr. Vivek
"""

import unittest
from dsa.seat_matrix import SeatMatrix, SeatTier, SeatStatus
from dsa.trie import MovieTrie
from dsa.bst import MovieBST
from dsa.waitlist_queue import FIFOQueue, PriorityWaitlist, WaitlistRequest
from dsa.cancellation_stack import BookingHistoryStack, BookingAction
from dsa.theatre_graph import TheatreGraph
from dsa.sorting import merge_sort, quick_sort
from dsa.hash_table import CustomHashTable


class TestCineSeatDSA(unittest.TestCase):

    def test_seat_matrix_and_adjacent_recommendation(self):
        matrix = SeatMatrix(rows=8, cols=5, base_price=250)
        self.assertEqual(matrix.get_available_seats_count(), 40)
        
        # Test Recliner seats suggestion (Rows G and H)
        suggested = matrix.suggest_best_adjacent_seats(count=2, preferred_tier="Recliner")
        self.assertEqual(len(suggested), 2)
        # Should pick central seats in back row H (e.g. H2, H3 or H3, H4)
        self.assertIn(suggested[0][0], ["G", "H"])
        self.assertIn(suggested[1][0], ["G", "H"])

        # Book the suggested seats
        success = matrix.book_seats(suggested, user_id="khushi@cineseat.edu", booking_id=101)
        self.assertTrue(success)
        self.assertEqual(matrix.get_available_seats_count(), 38)
        
        # Booking again should fail (duplicate seat prevention)
        duplicate_attempt = matrix.book_seats(suggested, user_id="other@user.com", booking_id=102)
        self.assertFalse(duplicate_attempt)

        # Release seats
        matrix.release_seats(suggested)
        self.assertEqual(matrix.get_available_seats_count(), 40)

    def test_movie_trie_search_and_autocomplete(self):
        trie = MovieTrie()
        m1 = {"id": 1, "name": "Pathaan", "genre": "Action"}
        m2 = {"id": 2, "name": "Jawan", "genre": "Action"}
        m3 = {"id": 3, "name": "Avengers: Doomsday", "genre": "Sci-Fi"}
        
        trie.insert("Pathaan", m1)
        trie.insert("Jawan", m2)
        trie.insert("Avengers: Doomsday", m3)

        # Prefix search
        res1 = trie.search_prefix("path")
        self.assertEqual(len(res1), 1)
        self.assertEqual(res1[0]["name"], "Pathaan")

        # Substring / token match (e.g. "Doomsday")
        res2 = trie.search_prefix("doom")
        self.assertEqual(len(res2), 1)
        self.assertEqual(res2[0]["name"], "Avengers: Doomsday")

        # Autocomplete
        auto = trie.autocomplete("j", limit=5)
        self.assertEqual(len(auto), 1)
        self.assertEqual(auto[0]["name"], "Jawan")

    def test_movie_bst_range_query(self):
        bst = MovieBST(key_name="rating")
        bst.insert(8.5, {"id": 1, "title": "Inception", "rating": 8.5})
        bst.insert(7.2, {"id": 2, "title": "Fighter", "rating": 7.2})
        bst.insert(9.0, {"id": 3, "title": "The Dark Knight", "rating": 9.0})
        bst.insert(6.8, {"id": 4, "title": "Action Movie", "rating": 6.8})

        # In-order traversal (ascending)
        inorder = bst.inorder_traversal(reverse=False)
        ratings = [m["rating"] for m in inorder]
        self.assertEqual(ratings, [6.8, 7.2, 8.5, 9.0])

        # Range query: ratings between 7.0 and 8.9
        filtered = bst.range_search(7.0, 8.9)
        filtered_ratings = [m["rating"] for m in filtered]
        self.assertIn(7.2, filtered_ratings)
        self.assertIn(8.5, filtered_ratings)
        self.assertNotIn(9.0, filtered_ratings)
        self.assertNotIn(6.8, filtered_ratings)

    def test_fifo_queue(self):
        queue = FIFOQueue()
        self.assertTrue(queue.is_empty())

        req1 = WaitlistRequest(1, "userA", "Alice", "show1", 2)
        req2 = WaitlistRequest(2, "userB", "Bob", "show1", 3)
        queue.enqueue(req1)
        queue.enqueue(req2)
        self.assertEqual(queue.size(), 2)

        popped = queue.dequeue()
        self.assertEqual(popped.user_id, "userA")
        self.assertEqual(queue.size(), 1)
        self.assertEqual(queue.peek().user_id, "userB")

    def test_priority_waitlist(self):
        pq = PriorityWaitlist()
        req_regular = WaitlistRequest(1, "regular", "Alice", "show1", 2, priority=10)
        req_vip = WaitlistRequest(2, "vip", "Bob", "show1", 2, priority=1)

        pq.push(req_regular)
        pq.push(req_vip)

        # VIP (priority=1) should be popped first
        top = pq.pop()
        self.assertEqual(top.user_id, "vip")
        second = pq.pop()
        self.assertEqual(second.user_id, "regular")

    def test_cancellation_stack(self):
        stack = BookingHistoryStack()
        action1 = BookingAction("BOOKING_CREATED", 1001, "userA", {"seats": ["A1", "A2"]})
        action2 = BookingAction("BOOKING_CANCELLED", 1001, "userA", {"seats": ["A1", "A2"]})

        stack.push(action1)
        stack.push(action2)
        self.assertEqual(stack.size(), 2)

        popped = stack.pop()
        self.assertEqual(popped.action_type, "BOOKING_CANCELLED")
        self.assertEqual(stack.peek().action_type, "BOOKING_CREATED")

    def test_theatre_graph_dijkstra(self):
        graph = TheatreGraph()
        # Find path from Karol Bagh to CineSeat Aurora (Saket)
        dist, path = graph.dijkstra_shortest_path("Karol Bagh", "Saket")
        self.assertLess(dist, float('inf'))
        self.assertEqual(path[0], "Karol Bagh")
        self.assertEqual(path[-1], "Saket")

        # Nearest theatre from Connaught Place should be CineSeat Citylight (0 km)
        nearest = graph.find_nearest_theatre("Connaught Place")
        self.assertEqual(nearest["nearest"]["theatreId"], "citylight")
        self.assertEqual(nearest["nearest"]["distanceKm"], 0.0)

    def test_custom_sorting_algorithms(self):
        movies = [
            {"name": "Alpha", "rating": 7.0, "price": 300},
            {"name": "Beta", "rating": 9.2, "price": 150},
            {"name": "Gamma", "rating": 8.4, "price": 250},
        ]

        # Merge sort by rating descending
        sorted_by_rating = merge_sort(movies, key_func=lambda m: m["rating"], reverse=True)
        self.assertEqual(sorted_by_rating[0]["name"], "Beta")
        self.assertEqual(sorted_by_rating[1]["name"], "Gamma")
        self.assertEqual(sorted_by_rating[2]["name"], "Alpha")

        # Quick sort by price ascending
        sorted_by_price = quick_sort(movies, key_func=lambda m: m["price"], reverse=False)
        self.assertEqual(sorted_by_price[0]["name"], "Beta")
        self.assertEqual(sorted_by_price[1]["name"], "Gamma")
        self.assertEqual(sorted_by_price[2]["name"], "Alpha")

    def test_custom_hash_table(self):
        ht = CustomHashTable()
        ht.insert("TICKET-9901", {"movie": "Pathaan", "seats": ["G3", "G4"]})
        ht.insert("TICKET-9902", {"movie": "Jawan", "seats": ["E1"]})

        self.assertTrue(ht.contains("TICKET-9901"))
        ticket = ht.get("TICKET-9901")
        self.assertEqual(ticket["movie"], "Pathaan")

        # Deletion
        self.assertTrue(ht.delete("TICKET-9901"))
        self.assertFalse(ht.contains("TICKET-9901"))


if __name__ == "__main__":
    unittest.main()
