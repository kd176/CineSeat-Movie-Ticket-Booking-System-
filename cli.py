"""
CineSeat - Interactive Python CLI & DSA Demonstration Terminal
Author: Khushi (Registration No. 251302194)
Teacher: Mr. Vivek
Course: Data Structures and Algorithms in Python
"""

import sys
import time
from typing import List

from engine.cinema_manager import CinemaManager
from engine.models import User
from dsa.seat_matrix import SeatStatus


def print_banner():
    banner = r"""
================================================================================
   ____ _            ____             _     ____  ____    _    
  / ___(_)_ __   ___/ ___|  ___  __ _| |_  |  _ \/ ___|  / \   
 | |   | | '_ \ / _ \___ \ / _ \/ _` | __| | | | \___ \ / _ \  
 | |___| | | | |  __/___) |  __/ (_| | |_  | |_| |___) / ___ \ 
  \____|_|_| |_|\___|____/ \___|\__,_|\__| |____/|____/_/   \_\
                                                               
   Movie Ticket Booking System - Python DSA Edition (Oct 2026)
   Student: Khushi | Reg No: 251302194 | Faculty: Mr. Vivek
================================================================================
"""
    print(banner)


def display_ascii_seat_grid(matrix, highlighted_seats=None):
    if highlighted_seats is None:
        highlighted_seats = []
    print("\n" + "=" * 50)
    print("                [ SCREEN THIS WAY ]")
    print("=" * 50)
    print("      Col 1    Col 2    Col 3    Col 4    Col 5")
    print("     -------------------------------------------")

    for r in range(matrix.num_rows):
        row_letter = chr(65 + r)
        tier_tag = " [Recliner]" if r >= 6 else (" [Premium] " if r >= 4 else " [Classic] ")
        row_str = f" {row_letter} | "
        for c in range(matrix.num_cols):
            seat = matrix.grid[r][c]
            if seat.label in highlighted_seats:
                cell = f"[* {seat.label} *]"
            elif seat.status == SeatStatus.BOOKED:
                cell = f"[  XX  ]"
            else:
                cell = f"[ {seat.label} ]"
            row_str += cell + " "
        row_str += tier_tag
        print(row_str)
    print("=" * 50)
    print(" Legend: [ G3 ] = Available | [  XX  ] = Booked | [* G3 *] = Selected")
    print("=" * 50 + "\n")


def main():
    cm = CinemaManager.get_instance()
    current_user = User("251302194", "Khushi", "khushi@cineseat.edu")
    selected_date = "2026-10-31"

    print_banner()
    print(f"Logged in as: {current_user.name} ({current_user.email}) | Reg: {current_user.user_id}\n")

    while True:
        print("\n--- MAIN MENU ---")
        print("1. Browse Movies (with Merge Sort / Quick Sort)")
        print("2. Search Movie with Trie (Prefix Autocomplete)")
        print("3. Filter Movies by Rating (Binary Search Tree Range Query)")
        print("4. Select Movie & View Show Experiences")
        print("5. View Cinema Hall 2D Seat Matrix & Suggest Best Recliners")
        print("6. Book Tickets (Atomic Multi-Seat Transaction)")
        print("7. My Tickets & Cancellation (LIFO Stack Rollback & Waitlist Reallocation)")
        print("8. Delhi NCR Theatres Route Finder (Dijkstra's Algorithm)")
        print("9. DSA Diagnostics & Viva Architecture Summary")
        print("0. Exit")

        choice = input("\nEnter choice [0-9]: ").strip()

        if choice == "1":
            print("\nSort by: 1. Rating (Merge Sort) | 2. Price (Quick Sort) | 3. Popularity Hype (Quick Sort)")
            sc = input("Choice: ").strip()
            if sc == "2":
                sorted_movies = cm.get_sorted_movies(sort_by="price", reverse=False)
            elif sc == "3":
                sorted_movies = cm.get_sorted_movies(sort_by="hype", reverse=True)
            else:
                sorted_movies = cm.get_sorted_movies(sort_by="rating", reverse=True)

            print(f"\nShowing Top 10 Movies (out of {len(sorted_movies)}):")
            print(f"{'ID':<4} {'Title':<28} {'Genre':<16} {'Rating':<8} {'Price (Rs)':<10}")
            print("-" * 70)
            for m in sorted_movies[:10]:
                print(f"{m['id']:<4} {m['name'][:26]:<28} {m['genre'][:14]:<16} {m['rating']:<8} Rs {m['price']:<8}")

        elif choice == "2":
            query = input("\nEnter title prefix to search (e.g. 'path', 'jaw', 'aven', 'kan'): ").strip()
            start_t = time.perf_counter()
            matches = cm.search_movies(query)
            elapsed_us = (time.perf_counter() - start_t) * 1e6
            print(f"\n[MovieTrie] Search completed in {elapsed_us:.2f} microseconds. Found {len(matches)} matches:")
            for m in matches[:8]:
                print(f" -> [{m['id']}] {m['name']} ({m['genre']}, {m['language']}) - Rating: {m['rating']}/10")

        elif choice == "3":
            try:
                min_r = float(input("\nEnter minimum rating (e.g. 7.5): ").strip())
                max_r = float(input("Enter maximum rating (e.g. 9.5): ").strip())
            except ValueError:
                print("Invalid numerical input.")
                continue

            start_t = time.perf_counter()
            filtered = cm.filter_by_rating_range(min_r, max_r)
            elapsed_us = (time.perf_counter() - start_t) * 1e6
            print(f"\n[MovieBST] Range Query [{min_r} - {max_r}] executed in {elapsed_us:.2f} microseconds. Found {len(filtered)} movies:")
            for m in filtered[:8]:
                print(f" -> {m['name']} | Rating: {m['rating']} | Genre: {m['genre']}")

        elif choice == "4":
            mid_str = input("\nEnter Movie ID (1 to 56): ").strip()
            if not mid_str.isdigit() or int(mid_str) not in cm.movies_by_id:
                print("Invalid Movie ID.")
                continue
            mid = int(mid_str)
            movie = cm.movies_by_id[mid]
            print(f"\nSelected: {movie['name']} ({movie['year']}) | Director: {movie['director']}")
            print(f"Synopsis: {movie['synopsis']}")
            shows = cm.get_performances(mid, selected_date)
            print(f"\nPerformances on {selected_date}:")
            for idx, s in enumerate(shows, 1):
                print(f"{idx}. {s['theatreName']} ({s['area']}) | Time: {s['time']} | Screen: {s['screen']} | Format: {s['format']} | Seats Free: {s['availableSeats']}/40 | Base Price: Rs {s['basePrice']}")

        elif choice == "5":
            mid_str = input("\nEnter Movie ID (1 to 56): ").strip()
            if not mid_str.isdigit() or int(mid_str) not in cm.movies_by_id:
                print("Invalid Movie ID.")
                continue
            shows = cm.get_performances(int(mid_str), selected_date)
            show = shows[0]
            matrix = cm.get_or_create_seat_matrix(show["id"])
            suggested = matrix.suggest_best_adjacent_seats(count=2, preferred_tier="Recliner")
            print(f"\n[SeatMatrix] Performance: {show['theatreName']} at {show['time']}")
            print(f"[Adjacent Recommendation Algorithm] Recommended 2 adjacent Recliner seats: {suggested}")
            display_ascii_seat_grid(matrix, highlighted_seats=suggested)

        elif choice == "6":
            mid_str = input("\nEnter Movie ID to book: ").strip()
            if not mid_str.isdigit() or int(mid_str) not in cm.movies_by_id:
                print("Invalid Movie ID.")
                continue
            shows = cm.get_performances(int(mid_str), selected_date)
            print("\nAvailable shows:")
            for idx, s in enumerate(shows, 1):
                print(f"{idx}. {s['theatreName']} - {s['time']}")
            s_idx = int(input("Select show [1-3]: ").strip()) - 1
            selected_show = shows[s_idx]

            matrix = cm.get_or_create_seat_matrix(selected_show["id"])
            suggested = matrix.suggest_best_adjacent_seats(count=2, preferred_tier="Recliner")
            display_ascii_seat_grid(matrix, highlighted_seats=suggested)

            seat_input = input(f"Enter comma-separated seats (Press Enter for suggested {suggested}): ").strip()
            if seat_input:
                chosen_seats = [s.strip().upper() for s in seat_input.split(",")]
            else:
                chosen_seats = suggested

            promo = input("Enter Promo Code (Try 'MOVIENIGHT' for 10% off): ").strip()
            payment_mode = input("Payment Method [1. UPI / 2. Card / 3. Cash]: ").strip()
            mode_name = "UPI" if payment_mode != "2" and payment_mode != "3" else ("Card" if payment_mode == "2" else "Cash")

            try:
                order = cm.create_booking_order(
                    user=current_user,
                    items=[{"showKey": selected_show["id"], "seats": chosen_seats}],
                    promo_code=promo,
                    payment_mode=mode_name
                )
                print("\n" + "*" * 60)
                print("           BOOKING CONFIRMED (ATOMIC TRANSACTION)")
                print("*" * 60)
                print(f" Order ID:    {order['orderId']}")
                print(f" Subtotal:    Rs {order['subtotal']:.2f}")
                print(f" Discount:    Rs {order['discount']:.2f}")
                print(f" Grand Total: Rs {order['grandTotal']:.2f} ({order['mode']})")
                for b in order["bookings"]:
                    print(f" Ticket #{b['id']}: {b['title']} | {b['theatreName']} | Seats: {b['seats']}")
                print("*" * 60)
            except Exception as e:
                print(f"\n[Error] Booking failed: {e}")

        elif choice == "7":
            bookings = cm.get_user_bookings(current_user.user_id)
            if not bookings:
                print("\nNo bookings found for user.")
                continue
            print("\nYour Bookings:")
            for b in bookings:
                status_icon = "[OK]" if b["status"] == "Confirmed" else "[CANCELLED]"
                print(f"Booking ID: {b['id']} | {b['title']} | {b['theatreName']} | Seats: {b['seats']} | Status: {status_icon}")
            
            cancel_id_str = input("\nEnter Booking ID to Cancel (or press Enter to return): ").strip()
            if cancel_id_str.isdigit():
                try:
                    res = cm.cancel_booking(int(cancel_id_str), current_user.user_id)
                    print(f"\n[BookingHistoryStack] Pushed cancellation action to LIFO Stack.")
                    print(f"Booking #{res['bookingId']} status: {res['status']}. Refund: Rs {res['refundAmount']}")
                    if res.get("waitlistReallocated"):
                        print(f" -> [FIFO Queue Automatic Allocation] Reallocated seats to waitlisted user: {res['waitlistReallocated']['user']}")
                except Exception as e:
                    print(f"Cancellation error: {e}")

        elif choice == "8":
            print("\nLocations: Connaught Place, Saket, Noida Sector 18, Karol Bagh, Cyber City, Nehru Place")
            user_hub = input("Enter your starting location: ").strip() or "Karol Bagh"
            nearest = cm.theatre_graph.find_nearest_theatre(user_hub)
            print(f"\n[TheatreGraph - Dijkstra's Algorithm] User Origin: {user_hub}")
            print(f"Nearest Venue: {nearest['nearest']['theatreName']} ({nearest['nearest']['area']})")
            print(f"Minimal Distance: {nearest['nearest']['distanceKm']} km | Approx Travel Time: {nearest['nearest']['travelMinutes']} mins")
            print(f"Shortest Road Route: {' -> '.join(nearest['nearest']['route'])}")

        elif choice == "9":
            diag = cm.get_dsa_diagnostics()
            print("\n" + "=" * 65)
            print("       CINESEAT PYTHON DSA SYSTEM DIAGNOSTICS & VIVA SUMMARY")
            print("=" * 65)
            for module, stats in diag.items():
                print(f"[*] {module}:")
                if isinstance(stats, dict):
                    for k, v in stats.items():
                        print(f"      {k}: {v}")
                else:
                    print(f"      {stats}")
            print("=" * 65)

        elif choice == "0":
            print("\nExiting CineSeat CLI. Goodbye!")
            sys.exit(0)


if __name__ == "__main__":
    main()
