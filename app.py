"""
CineSeat - Movie Ticket Booking System (Python DSA Backend + Original CineSeat UI)
Student: Khushi (Registration No. 251302194)
Teacher: Mr. Vivek
Course: Data Structures and Algorithms in Python
"""

import os
import json
import time
from datetime import datetime, timezone, timedelta
from flask import Flask, jsonify, request, send_from_directory, render_template_string
from flask_cors import CORS

from engine.cinema_manager import CinemaManager
from engine.models import User

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "public", "web")
POSTERS_DIR = os.path.join(BASE_DIR, "public", "posters")

app = Flask(__name__)
CORS(app)

cm = CinemaManager.get_instance()

# Default Student Authenticated User
DEMO_USER = {
    "id": "251302194",
    "name": "Khushi",
    "email": "khushi@cineseat.edu",
    "isAdmin": True
}


def now_iso():
    return datetime.now(timezone.utc).isoformat()


@app.route("/web/<path:filename>")
def serve_web(filename):
    return send_from_directory(WEB_DIR, filename)


@app.route("/posters/<path:filename>")
def serve_posters(filename):
    return send_from_directory(POSTERS_DIR, filename)


@app.route("/project-guide.html")
def serve_project_guide():
    return send_from_directory(os.path.join(BASE_DIR, "public"), "project-guide.html")


# Exact Original CineSeat Frontend Shell
ORIGINAL_HTML_SHELL = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CineSeat · Shared Cinema Booking</title>
  <link rel="stylesheet" href="/web/style.css">
  <link rel="stylesheet" href="/web/final.css">
  <style>
    /* DSA Inspection Floating Pill for Mr. Vivek */
    .dsa-pill {
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: #c7e998;
      color: #10190f;
      padding: 10px 18px;
      border-radius: 30px;
      font-size: 13px;
      font-weight: 800;
      box-shadow: 0 4px 20px rgba(0,0,0,0.6);
      z-index: 9999;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      border: 2px solid #16220e;
      text-decoration: none;
    }
    .dsa-pill:hover { background: #dbf4b3; }
  </style>
</head>
<body>
  <header>
    <a class="brand" href="#" onclick="go('movies');return false">▣ <span>Cine<span class="accent">Seat</span></span></a>
    <nav>
      <button data-nav="movies" onclick="go('movies')" class="active">Discover</button>
      <button data-nav="bookings" onclick="go('bookings')">My tickets</button>
      <button data-nav="saved" onclick="go('saved')">Watchlist</button>
      <button data-nav="admin" onclick="go('admin')">Admin</button>
    </nav>
    <button class="cart-nav" onclick="go('cart')">Bag <span id="bag-count">0</span></button>
    <button class="account" id="account" onclick="account()">Khushi ↗</button>
  </header>

  <main id="app">
    <div class="empty"><h2>Getting the cinema ready…</h2><p>Connecting to the shared box office.</p></div>
  </main>

  <footer>
    <a class="brand" href="#">▣ CineSeat</a>
    <span>A little escape. A great story.</span>
    <small>DSA project · Khushi · 251302194 · Faculty: Mr. Vivek<br>Demo payments · Shared cloud bookings · India show times · Pure Python DSA Engine</small>
  </footer>

  <dialog id="modal"></dialog>
  <div id="toast" role="status"></div>

  <!-- Floating shortcut to inspect DSA diagnostics if needed -->
  <a href="/project-guide.html" target="_blank" class="dsa-pill">
    ⚡ Academic Guide & Demo Script
  </a>

  <!-- Original CineSeat Scripts in exact sequence -->
  <script src="/web/app.js"></script>
  <script src="/web/upgrade.js"></script>
  <script src="/web/discovery.js"></script>
  <script src="/web/cloud.js"></script>
  <script src="/web/final.js"></script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(ORIGINAL_HTML_SHELL)


# API Endpoints compatible with cloud.js, final.js, and app.js
@app.route("/api/state", methods=["GET"])
def api_state():
    """State endpoint supplying 56 movies, theatres, releases, bookings, and user identity."""
    movies_json = []
    cat_path = os.path.join(BASE_DIR, "server", "catalogue.json")
    enr_path = os.path.join(BASE_DIR, "server", "enrichment.json")
    cat = json.load(open(cat_path, encoding="utf-8")) if os.path.exists(cat_path) else []
    enr = json.load(open(enr_path, encoding="utf-8")) if os.path.exists(enr_path) else {}

    for m in cat:
        mid = m["id"]
        extra = enr.get(str(mid), {})
        m_copy = dict(m)
        m_copy.update(extra)
        m_copy["id"] = mid
        m_copy["price"] = m.get("price", 250)
        m_copy["seats"] = m.get("seats", 10)
        m_copy["version"] = 1
        m_copy["poster"] = f"/posters/{mid}.jpg" if os.path.exists(os.path.join(POSTERS_DIR, f"{mid}.jpg")) else m.get("art")
        movies_json.append(m_copy)

    # Bookings and Orders
    bookings_json = [b.to_dict() for b in cm.bookings]
    orders_json = []
    occupied = []

    # Populate occupied seat claims
    for show_key, matrix in cm.seat_matrices.items():
        for r in range(matrix.num_rows):
            for c in range(matrix.num_cols):
                seat = matrix.grid[r][c]
                if seat.status.value == "Booked":
                    occupied.append({
                        "show_key": show_key,
                        "seat": (r * matrix.num_cols) + (c + 1)
                    })

    # Theatres config matching experiences.mjs
    theatres_data = [
        {
            "id": "citylight",
            "name": "CineSeat Citylight",
            "area": "Connaught Place",
            "city": "Delhi NCR",
            "address": "Demo venue · Central Delhi",
            "format": "2D",
            "projection": "HD / 2K",
            "audio": "Dolby 7.1",
            "subtitles": "None",
            "premium": 0,
            "amenities": ["Parking", "Food court", "Wheelchair access"]
        },
        {
            "id": "aurora",
            "name": "CineSeat Aurora",
            "area": "Saket",
            "city": "Delhi NCR",
            "address": "Demo venue · South Delhi",
            "format": "2D",
            "projection": "4K Laser",
            "audio": "Dolby Atmos",
            "subtitles": "English",
            "premium": 80,
            "amenities": ["Parking", "Lounge", "Recliners", "Wheelchair access"]
        },
        {
            "id": "horizon",
            "name": "CineSeat Horizon",
            "area": "Noida",
            "city": "Delhi NCR",
            "address": "Demo venue · Noida",
            "format": "3D",
            "projection": "HD / 2K",
            "audio": "Dolby Atmos",
            "subtitles": "None",
            "premium": 120,
            "amenities": ["Parking", "Food court", "Recliners", "Wheelchair access"]
        }
    ]

    return jsonify({
        "current": DEMO_USER,
        "movies": movies_json,
        "bookings": bookings_json,
        "orders": orders_json,
        "occupied": occupied,
        "waiting": [],
        "users": [DEMO_USER],
        "favourites": {},
        "hypeVotes": {},
        "hypeTotals": {m["id"]: {"votes": 10, "saves": 5, "seats": 8, "score": 85} for m in cat},
        "stack": [b.booking_id for b in cm.bookings if b.status == "Cancelled"],
        "queues": {},
        "showQueues": {},
        "version2": True,
        "discoveryVersion": 1,
        "timezone": "Asia/Kolkata",
        "serverTime": now_iso(),
        "theatres": theatres_data,
        "releases": cm.releases,
        "ratings": {m["id"]: {"average": round(7.5 + (m["id"] % 20) * 0.1, 1), "count": 25} for m in cat},
        "myRatings": {}
    })


@app.route("/api/sessions", methods=["GET"])
def api_sessions():
    movie_id = request.args.get("movie", type=int)
    date = request.args.get("date", "2026-10-31").strip()
    if not movie_id or movie_id not in cm.movies_by_id:
        return jsonify({"error": "Movie not found"}), 404

    movie = cm.movies_by_id[movie_id]
    perf_times = ["10:00", "14:00", "18:00", "22:00"]
    theatres = cm.theatres

    shows = []
    for idx, venue in enumerate(theatres):
        time_slot = perf_times[(movie_id - 1 + idx) % 4]
        is_3d = venue["format"] == "3D" and any(g in movie["genre"] for g in ["Animation", "Sci-Fi", "Adventure", "Action"])
        fmt = "3D" if is_3d else "2D"
        prem = 80 if (idx == 2 and not is_3d) else (venue["premium"] * 100)
        base = int(movie["price"] * 100) + prem
        show_id = f"{movie_id}|{date}|{time_slot}|{venue['id']}"

        # 40 seat prices
        seat_prices = []
        for s in range(40):
            kind = "Recliner" if s >= 30 else ("Premium" if s >= 20 else "Classic")
            surcharge = 20000 if kind == "Recliner" else (6000 if kind == "Premium" else 0)
            seat_prices.append({
                "seat": s + 1,
                "label": f"{chr(65 + (s // 5))}{(s % 5) + 1}",
                "kind": kind,
                "price": base + surcharge
            })

        matrix = cm.get_or_create_seat_matrix(show_id)
        occ = []
        for r in range(matrix.num_rows):
            for c in range(matrix.num_cols):
                if matrix.grid[r][c].status.value == "Booked":
                    occ.append((r * matrix.num_cols) + (c + 1))

        shows.append({
            "id": show_id,
            "movie": movie_id,
            "date": date,
            "time": time_slot,
            "theatre": venue["id"],
            "theatreName": venue["name"],
            "area": venue["area"],
            "city": venue["city"],
            "screen": f"Screen {((movie_id - 1) // 4) + 1}",
            "language": movie.get("language", "Hindi"),
            "dubbed": False,
            "subtitles": venue.get("subtitles", "English"),
            "format": fmt,
            "projection": venue.get("projection", "HD / 2K"),
            "audio": venue.get("audio", "Dolby 7.1"),
            "amenities": venue.get("amenities", []),
            "capacity": 40,
            "fromPrice": base,
            "seatPrices": seat_prices,
            "occupied": occ,
            "started": False,
            "demo": True
        })

    return jsonify({"movie": movie, "shows": shows})


@app.route("/api/trending", methods=["GET"])
def api_trending():
    period = request.args.get("period", "week")
    return jsonify({
        "source": "Simkl",
        "period": period,
        "cached": True,
        "items": [
            {"rank": i + 1, "title": m["name"], "year": m["year"], "watchers": 1500 - i * 20, "url": "https://simkl.com", "poster": m.get("poster")}
            for i, m in enumerate(cm.movies[:20])
        ]
    })


@app.route("/api/checkout", methods=["POST"])
def api_checkout():
    body = request.get_json() or {}
    items = body.get("items", [])
    snacks = body.get("snacks", 0)
    promo = body.get("promo", "")
    mode = body.get("mode", "UPI")

    # Map original checkout payload to CinemaManager
    manager_items = []
    for it in items:
        perf_id = it.get("performanceId")
        seats = it.get("seats", [])
        seat_labels = [f"{chr(65 + ((s - 1) // 5))}{((s - 1) % 5) + 1}" for s in seats]
        manager_items.append({"showKey": perf_id, "seats": seat_labels})

    try:
        user_obj = User(DEMO_USER["id"], DEMO_USER["name"], DEMO_USER["email"])
        order = cm.create_booking_order(
            user=user_obj,
            items=manager_items,
            snacks_count=snacks,
            promo_code=promo,
            payment_mode=mode
        )
        return jsonify({
            "order": {
                "id": order["orderId"],
                "total": order["grandTotal"],
                "subtotal": order["subtotal"],
                "discount": order["discount"],
                "status": "Confirmed",
                "payment": "Paid",
                "mode": mode,
                "bookings": [b["id"] for b in order["bookings"]]
            },
            "replayed": False
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/cancel", methods=["POST"])
def api_cancel():
    body = request.get_json() or {}
    order_id = body.get("order")
    # Cancel bookings under this order
    bookings_to_cancel = [b for b in cm.bookings if b.order_id == order_id]
    for b in bookings_to_cancel:
        cm.cancel_booking(b.booking_id, DEMO_USER["id"])
    return jsonify({"ok": True})


@app.route("/api/rating", methods=["POST"])
@app.route("/api/vote", methods=["POST"])
@app.route("/api/favourite", methods=["POST"])
def api_preferences():
    return jsonify({"ok": True})


if __name__ == "__main__":
    port = 5000
    print(f"================================================================")
    print(f" CineSeat Original Website + Python DSA Engine Running!")
    print(f" Student: Khushi (Reg No: 251302194) | Faculty: Mr. Vivek")
    print(f" Open in browser: http://127.0.0.1:{port}")
    print(f"================================================================")
    app.run(host="0.0.0.0", port=port, debug=False)
