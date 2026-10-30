"""
Data Models for CineSeat Engine
Module: engine.models
"""

from typing import List, Dict, Any, Optional
import time


class User:
    def __init__(self, user_id: str, name: str, email: str, is_admin: bool = False):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.is_admin = is_admin

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.user_id,
            "name": self.name,
            "email": self.email,
            "isAdmin": self.is_admin
        }


class Booking:
    def __init__(
        self,
        booking_id: int,
        order_id: int,
        user_id: str,
        user_name: str,
        movie_id: int,
        movie_title: str,
        show_key: str,
        theatre_id: str,
        theatre_name: str,
        date: str,
        time_slot: str,
        screen: str,
        format_type: str,
        seats: List[str],
        total_amount: float,
        status: str = "Confirmed",
        payment_mode: str = "UPI"
    ):
        self.booking_id = booking_id
        self.order_id = order_id
        self.user_id = user_id
        self.user_name = user_name
        self.movie_id = movie_id
        self.movie_title = movie_title
        self.show_key = show_key
        self.theatre_id = theatre_id
        self.theatre_name = theatre_name
        self.date = date
        self.time_slot = time_slot
        self.screen = screen
        self.format_type = format_type
        self.seats = seats
        self.total_amount = total_amount
        self.status = status
        self.payment_mode = payment_mode
        self.created_at = time.strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.booking_id,
            "orderId": self.order_id,
            "userId": self.user_id,
            "userName": self.user_name,
            "movieId": self.movie_id,
            "title": self.movie_title,
            "showKey": self.show_key,
            "theatreId": self.theatre_id,
            "theatreName": self.theatre_name,
            "date": self.date,
            "time": self.time_slot,
            "screen": self.screen,
            "format": self.format_type,
            "seats": self.seats,
            "price": self.total_amount,
            "status": self.status,
            "payment": "Paid" if self.status == "Confirmed" else "Refunded",
            "mode": self.payment_mode,
            "created": self.created_at
        }
