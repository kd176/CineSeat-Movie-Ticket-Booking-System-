"""
Seat Matrix and Adjacent Recommendation Algorithm
Module: dsa.seat_matrix
Academic Concept: 2D Arrays / Matrices, Spatial Search, Sliding Window Algorithm

Time Complexity:
- Matrix Access / Update: O(1)
- Best Adjacent Seats Suggestion: O(R * C) where R is rows and C is columns
Space Complexity: O(R * C) for grid representation
"""

from enum import Enum
from typing import List, Optional, Tuple, Dict, Any


class SeatTier(str, Enum):
    CLASSIC = "Classic"      # Rows A - D
    PREMIUM = "Premium"      # Rows E - F (+₹60)
    RECLINER = "Recliner"    # Rows G - H (+₹200)


class SeatStatus(str, Enum):
    AVAILABLE = "Available"
    BOOKED = "Booked"
    LOCKED = "Locked"


class Seat:
    def __init__(self, row_idx: int, col_idx: int, tier: SeatTier, base_price: int, tier_surcharge: int):
        self.row_idx = row_idx
        self.col_idx = col_idx
        self.row_letter = chr(65 + row_idx)  # 0 -> 'A', 1 -> 'B', etc.
        self.col_number = col_idx + 1        # 1-indexed
        self.label = f"{self.row_letter}{self.col_number}"
        self.tier = tier
        self.price = base_price + tier_surcharge
        self.status = SeatStatus.AVAILABLE
        self.booked_by: Optional[str] = None
        self.booking_id: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "label": self.label,
            "row": self.row_letter,
            "col": self.col_number,
            "tier": self.tier.value,
            "price": self.price,
            "status": self.status.value,
            "bookedBy": self.booked_by
        }


class SeatMatrix:
    """
    2D Matrix representation of a Cinema Hall layout.
    Default Dimensions: 8 Rows (A-H), 5 Columns (1-5) = 40 Seats.
    - Rows A-D (indices 0..3): Classic
    - Rows E-F (indices 4..5): Premium (+₹60)
    - Rows G-H (indices 6..7): Recliner (+₹200)
    """

    def __init__(self, rows: int = 8, cols: int = 5, base_price: int = 250):
        self.num_rows = rows
        self.num_cols = cols
        self.base_price = base_price
        self.total_capacity = rows * cols
        
        # Initialize 2D Grid: grid[row][col]
        self.grid: List[List[Seat]] = []
        for r in range(rows):
            row_seats: List[Seat] = []
            tier = SeatTier.RECLINER if r >= 6 else (SeatTier.PREMIUM if r >= 4 else SeatTier.CLASSIC)
            surcharge = 200 if tier == SeatTier.RECLINER else (60 if tier == SeatTier.PREMIUM else 0)
            
            for c in range(cols):
                seat = Seat(row_idx=r, col_idx=c, tier=tier, base_price=base_price, tier_surcharge=surcharge)
                row_seats.append(seat)
            self.grid.append(row_seats)

    def _parse_label(self, label: str) -> Tuple[int, int]:
        """Convert 'G3' -> (row=6, col=2). O(1) Time."""
        label = label.strip().upper()
        if len(label) < 2:
            raise ValueError(f"Invalid seat label format: {label}")
        row_letter = label[0]
        col_str = label[1:]
        row_idx = ord(row_letter) - 65
        col_idx = int(col_str) - 1
        
        if not (0 <= row_idx < self.num_rows and 0 <= col_idx < self.num_cols):
            raise IndexError(f"Seat {label} out of bounds.")
        return row_idx, col_idx

    def get_seat(self, label: str) -> Seat:
        """Lookup seat by label in O(1) time."""
        r, c = self._parse_label(label)
        return self.grid[r][c]

    def book_seats(self, labels: List[str], user_id: str, booking_id: int) -> bool:
        """
        Atomically reserve a list of seats.
        If any seat is already booked, transaction rolls back.
        Time Complexity: O(K) where K is number of seats.
        """
        # Validate availability first
        for label in labels:
            seat = self.get_seat(label)
            if seat.status != SeatStatus.AVAILABLE:
                return False
        
        # Commit reservations
        for label in labels:
            seat = self.get_seat(label)
            seat.status = SeatStatus.BOOKED
            seat.booked_by = user_id
            seat.booking_id = booking_id
        return True

    def release_seats(self, labels: List[str]) -> None:
        """Free previously booked seats. O(K) Time."""
        for label in labels:
            try:
                seat = self.get_seat(label)
                seat.status = SeatStatus.AVAILABLE
                seat.booked_by = None
                seat.booking_id = None
            except (ValueError, IndexError):
                continue

    def get_available_seats_count(self) -> int:
        """Count total available seats. O(R * C) Time."""
        count = 0
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if self.grid[r][c].status == SeatStatus.AVAILABLE:
                    count += 1
        return count

    def suggest_best_adjacent_seats(self, count: int = 2, preferred_tier: Optional[str] = None) -> List[str]:
        """
        Adjacent Seat Recommendation Algorithm (Sliding Window & Spatial Scoring).
        
        Problem: Find 'count' contiguous free seats in a single row that maximize
        the audience's viewing quality (minimizing distance from screen center).
        
        Algorithm:
        1. Filter target rows matching preferred_tier (e.g., Recliner -> Rows G, H).
           If not found or unavailable, fall back to any tier.
        2. Within each row, apply a sliding window of size `count`.
        3. Check if all seats in window are AVAILABLE.
        4. Calculate window score based on:
           - Center alignment: distance of window center from middle column ((cols - 1) / 2)
           - Back-row preference: higher rows have better screen viewing angle.
        5. Return the seat labels of the candidate with the lowest penalty score.
        
        Time Complexity: O(R * C)
        Space Complexity: O(count) auxiliary
        """
        if count <= 0 or count > self.num_cols:
            return []

        target_tier = preferred_tier.title() if preferred_tier else None
        
        # Decide row scanning order: check requested tier rows first
        row_indices = []
        if target_tier == "Recliner":
            row_indices = [7, 6]  # Row H, Row G
        elif target_tier == "Premium":
            row_indices = [5, 4]  # Row F, Row E
        elif target_tier == "Classic":
            row_indices = [3, 2, 1, 0]  # Rows D, C, B, A
        else:
            # Default priority: Recliners first, then Premium, then Classic
            row_indices = [7, 6, 5, 4, 3, 2, 1, 0]

        center_col = (self.num_cols - 1) / 2.0
        best_candidate: Optional[List[Seat]] = None
        best_score = float('inf')

        def evaluate_rows(rows_to_check: List[int]) -> Optional[List[str]]:
            nonlocal best_candidate, best_score
            for r in rows_to_check:
                row = self.grid[r]
                # Sliding window of size `count` across columns
                for start_c in range(self.num_cols - count + 1):
                    window = row[start_c : start_c + count]
                    # Check if all seats in candidate window are available
                    if all(s.status == SeatStatus.AVAILABLE for s in window):
                        # Center distance penalty
                        window_center = start_c + (count - 1) / 2.0
                        col_distance = abs(window_center - center_col)
                        
                        # Row penalty: slightly favor higher rows (better viewing depth)
                        row_penalty = (self.num_rows - 1 - r) * 0.1
                        
                        total_score = col_distance + row_penalty
                        if total_score < best_score:
                            best_score = total_score
                            best_candidate = window
            return [s.label for s in best_candidate] if best_candidate else None

        # Pass 1: Try requested tier
        result = evaluate_rows(row_indices)
        if result:
            return result

        # Pass 2: Fallback across any available row
        all_rows = [7, 6, 5, 4, 3, 2, 1, 0]
        result = evaluate_rows(all_rows)
        return result if result else []

    def export_grid(self) -> List[List[Dict[str, Any]]]:
        """Serialize 2D grid for frontend UI rendering."""
        return [[seat.to_dict() for seat in row] for row in self.grid]
