"""
CineSeat - Movie Ticket Booking System (Python DSA Web Edition)
Student: Khushi (Registration No. 251302194)
Teacher: Mr. Vivek
Course: Data Structures and Algorithms in Python

Run locally:
    python app.py
Open:
    http://127.0.0.1:5000
"""

import os
from flask import Flask, jsonify, request, send_from_directory, render_template_string
from flask_cors import CORS

from engine.cinema_manager import CinemaManager
from engine.models import User

# Initialize Flask app
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTERS_DIR = os.path.join(BASE_DIR, "public", "posters")

app = Flask(__name__)
CORS(app)

# Initialize Cinema Manager Singleton
cm = CinemaManager.get_instance()

# Default Demo User
DEMO_USER = User(user_id="251302194", name="Khushi", email="khushi@cineseat.edu")


@app.route("/posters/<path:filename>")
def serve_poster(filename):
    """Serve movie posters directly from public/posters/."""
    if os.path.exists(os.path.join(POSTERS_DIR, filename)):
        return send_from_directory(POSTERS_DIR, filename)
    return "", 404


@app.route("/api/user", methods=["GET"])
def get_user():
    return jsonify(DEMO_USER.to_dict())


@app.route("/api/movies", methods=["GET"])
def get_movies():
    """
    Fetch movies using DSA components:
    - Search prefix query -> MovieTrie (O(L))
    - Sorting -> Merge Sort (Rating, Name) or Quick Sort (Price, Hype) (O(N log N))
    - Rating Range -> MovieBST Range Query (O(log N + K))
    """
    query = request.args.get("query", "").strip()
    sort_by = request.args.get("sortBy", "rating").strip()
    genre = request.args.get("genre", "").strip()
    min_rating = request.args.get("minRating", type=float)
    max_rating = request.args.get("maxRating", type=float)

    # 1. Search via Trie if query provided
    if query:
        movie_list = cm.search_movies(query)
    elif min_rating is not None and max_rating is not None:
        movie_list = cm.filter_by_rating_range(min_rating, max_rating)
    else:
        movie_list = cm.get_sorted_movies(sort_by=sort_by, reverse=(sort_by != "price"))

    # Optional genre filter
    if genre and genre.lower() != "all":
        movie_list = [m for m in movie_list if genre.lower() in m.get("genre", "").lower()]

    return jsonify({
        "count": len(movie_list),
        "movies": movie_list,
        "dsaMethodUsed": f"MovieTrie (Search: '{query}')" if query else (f"MovieBST Range [{min_rating}-{max_rating}]" if min_rating else f"Sorting ({sort_by})")
    })


@app.route("/api/movies/<int:movie_id>", methods=["GET"])
def get_movie_detail(movie_id):
    movie = cm.movies_by_id.get(movie_id)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404
    return jsonify(movie)


@app.route("/api/releases", methods=["GET"])
def get_releases():
    return jsonify(cm.releases)


@app.route("/api/shows", methods=["GET"])
def get_shows():
    movie_id = request.args.get("movieId", type=int)
    date = request.args.get("date", "2026-10-31").strip()
    if not movie_id:
        return jsonify({"error": "movieId is required"}), 400
    shows = cm.get_performances(movie_id, date)
    return jsonify(shows)


@app.route("/api/seats", methods=["GET"])
def get_seats():
    show_key = request.args.get("showKey", "").strip()
    if not show_key:
        return jsonify({"error": "showKey is required"}), 400
    matrix = cm.get_or_create_seat_matrix(show_key)
    return jsonify({
        "showKey": show_key,
        "capacity": matrix.total_capacity,
        "availableCount": matrix.get_available_seats_count(),
        "grid": matrix.export_grid()
    })


@app.route("/api/suggest-seats", methods=["GET"])
def suggest_seats():
    """Trigger Adjacent Seat Recommendation Algorithm (Sliding Window on 2D Matrix)."""
    show_key = request.args.get("showKey", "").strip()
    count = request.args.get("count", 2, type=int)
    tier = request.args.get("tier", "Recliner").strip()
    
    suggested = cm.suggest_adjacent_seats(show_key, count=count, tier=tier)
    return jsonify({
        "showKey": show_key,
        "requestedCount": count,
        "preferredTier": tier,
        "suggestedSeats": suggested,
        "algorithm": "Sliding Window Spatial Scoring - O(R * C)"
    })


@app.route("/api/checkout", methods=["POST"])
def checkout():
    """Atomic booking transaction with custom hash table and LIFO stack auditing."""
    data = request.get_json() or {}
    items = data.get("items", [])
    snacks = data.get("snacks", 0)
    promo = data.get("promo", "")
    mode = data.get("mode", "UPI")

    try:
        order = cm.create_booking_order(
            user=DEMO_USER,
            items=items,
            snacks_count=snacks,
            promo_code=promo,
            payment_mode=mode
        )
        return jsonify({"success": True, "order": order})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/my-bookings", methods=["GET"])
def my_bookings():
    bookings = cm.get_user_bookings(DEMO_USER.user_id)
    return jsonify(bookings)


@app.route("/api/cancel-booking", methods=["POST"])
def cancel_booking():
    """Cancel booking, update LIFO stack, and trigger automatic FIFO waitlist allocation."""
    data = request.get_json() or {}
    booking_id = data.get("bookingId")
    if not booking_id:
        return jsonify({"error": "bookingId is required"}), 400
    try:
        res = cm.cancel_booking(int(booking_id), DEMO_USER.user_id)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/waitlist", methods=["POST"])
def join_waitlist():
    """Join FIFO Waiting List Queue."""
    data = request.get_json() or {}
    show_key = data.get("showKey")
    count = data.get("seatCount", 2)
    if not show_key:
        return jsonify({"error": "showKey is required"}), 400
    res = cm.join_waitlist(DEMO_USER, show_key, int(count))
    return jsonify(res)


@app.route("/api/theatres/nearest", methods=["GET"])
def nearest_theatre():
    """Run Dijkstra's Algorithm on Delhi NCR Road Graph."""
    hub = request.args.get("hub", "Connaught Place").strip()
    result = cm.theatre_graph.find_nearest_theatre(hub)
    return jsonify(result)


@app.route("/api/dsa-diagnostics", methods=["GET"])
def dsa_diagnostics():
    """Comprehensive diagnostic metrics for viva and evaluation."""
    diag = cm.get_dsa_diagnostics()
    diag["theatreNetwork"] = cm.theatre_graph.get_network_graph()
    diag["cancellationHistory"] = cm.history_stack.get_history(limit=10)
    return jsonify(diag)


# Frontend HTML Template (Sleek dark-mode Cinema Web Interface)
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CineSeat · Python DSA Movie Ticket Booking System</title>
  <style>
    :root {
      --bg: #10190f;
      --card-bg: #1a2717;
      --surface: #22331f;
      --accent: #c7e998;
      --accent-hover: #dbf4b3;
      --text: #edf2e7;
      --muted: #a4b799;
      --border: #32472b;
      --danger: #ff6b6b;
      --warning: #f1c40f;
      --booked: #4a5c43;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    body { background-color: var(--bg); color: var(--text); min-height: 100vh; }
    
    /* Top Banner */
    .top-bar {
      background: #0b120a;
      border-bottom: 1px solid var(--border);
      padding: 10px 24px;
      font-size: 13px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: var(--muted);
    }
    .top-bar strong { color: var(--accent); }

    /* Header */
    header {
      background: var(--card-bg);
      border-bottom: 1px solid var(--border);
      padding: 16px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 100;
    }
    .brand { display: flex; align-items: center; gap: 12px; }
    .brand-logo { font-size: 26px; font-weight: 800; color: var(--accent); letter-spacing: -1px; }
    .brand-tag { font-size: 12px; background: var(--surface); padding: 4px 8px; border-radius: 6px; border: 1px solid var(--border); }
    
    .nav-links { display: flex; gap: 12px; }
    .nav-btn {
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text);
      padding: 8px 16px;
      border-radius: 8px;
      cursor: pointer;
      font-weight: 600;
      font-size: 14px;
      transition: all 0.2s;
    }
    .nav-btn.active, .nav-btn:hover { background: var(--accent); color: #10190f; border-color: var(--accent); }

    /* Main Container */
    main { max-width: 1280px; margin: 0 auto; padding: 24px; }

    /* Search & Filter Bar */
    .filter-section {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 18px 20px;
      margin-bottom: 28px;
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      align-items: center;
      justify-content: space-between;
    }
    .search-box { flex: 1; min-width: 280px; position: relative; }
    .search-box input {
      width: 100%;
      background: var(--surface);
      border: 1px solid var(--border);
      padding: 12px 16px;
      border-radius: 8px;
      color: var(--text);
      font-size: 15px;
    }
    .search-box input:focus { outline: none; border-color: var(--accent); }
    .search-hint { font-size: 11px; color: var(--accent); margin-top: 4px; }

    .control-group { display: flex; gap: 12px; align-items: center; }
    select {
      background: var(--surface);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 10px 14px;
      border-radius: 8px;
      font-size: 14px;
      cursor: pointer;
    }

    /* Movie Grid */
    .movie-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 24px;
    }
    .movie-card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: transform 0.2s, border-color 0.2s;
    }
    .movie-card:hover { transform: translateY(-4px); border-color: var(--accent); }
    .poster-box { height: 360px; background: #000; overflow: hidden; position: relative; }
    .poster-box img { width: 100%; height: 100%; object-fit: cover; }
    .poster-badge {
      position: absolute;
      top: 10px;
      right: 10px;
      background: rgba(16, 25, 15, 0.85);
      border: 1px solid var(--border);
      padding: 4px 8px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      color: var(--accent);
    }
    .card-body { padding: 16px; display: flex; flex-direction: column; flex: 1; }
    .movie-title { font-size: 18px; font-weight: 700; margin-bottom: 6px; }
    .movie-meta { font-size: 13px; color: var(--muted); margin-bottom: 12px; }
    .movie-synopsis { font-size: 13px; color: #b7c8ae; margin-bottom: 16px; line-height: 1.4; flex: 1; }
    .card-actions { display: flex; gap: 8px; }
    .btn {
      flex: 1;
      padding: 10px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 14px;
      border: none;
      cursor: pointer;
      text-align: center;
      transition: background 0.2s;
    }
    .btn-primary { background: var(--accent); color: #10190f; }
    .btn-primary:hover { background: var(--accent-hover); }
    .btn-secondary { background: var(--surface); color: var(--text); border: 1px solid var(--border); }
    .btn-secondary:hover { background: #2f452a; }

    /* Modals & Overlays */
    .modal-overlay {
      position: fixed;
      top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0,0,0,0.8);
      display: none;
      justify-content: center;
      align-items: center;
      z-index: 200;
      padding: 20px;
    }
    .modal-overlay.open { display: flex; }
    .modal-content {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 14px;
      max-width: 850px;
      width: 100%;
      max-height: 90vh;
      overflow-y: auto;
      padding: 24px;
      position: relative;
    }
    .modal-close {
      position: absolute;
      top: 16px; right: 16px;
      background: transparent;
      border: none;
      color: var(--muted);
      font-size: 24px;
      cursor: pointer;
    }

    /* Seat Matrix View */
    .seat-screen {
      background: linear-gradient(to bottom, #32472b, transparent);
      height: 24px;
      border-radius: 12px 12px 0 0;
      text-align: center;
      font-size: 12px;
      color: var(--accent);
      line-height: 24px;
      letter-spacing: 2px;
      margin: 20px 0 24px;
      border-top: 2px solid var(--accent);
    }
    .seat-grid {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 10px;
      max-width: 480px;
      margin: 0 auto 24px;
    }
    .seat-cell {
      height: 44px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 6px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 12px;
      font-weight: 700;
      transition: all 0.15s;
    }
    .seat-cell:hover:not(.booked) { border-color: var(--accent); transform: scale(1.05); }
    .seat-cell.selected { background: var(--accent); color: #10190f; border-color: var(--accent); }
    .seat-cell.booked { background: var(--booked); color: #6b7d65; cursor: not-allowed; border-color: #3b4b35; }
    .seat-cell.suggested { border: 2px dashed var(--accent); }

    /* Legend */
    .seat-legend { display: flex; justify-content: center; gap: 20px; font-size: 13px; margin-bottom: 20px; }
    .legend-item { display: flex; align-items: center; gap: 6px; }
    .legend-color { width: 16px; height: 16px; border-radius: 4px; border: 1px solid var(--border); }

    /* Diagnostics Table */
    table { width: 100%; border-collapse: collapse; margin-top: 14px; font-size: 14px; }
    th, td { padding: 12px; text-align: left; border-bottom: 1px solid var(--border); }
    th { color: var(--accent); background: var(--surface); }
    .badge { padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; }
    .badge-success { background: #234d20; color: #a3e635; }
    .badge-danger { background: #4d2020; color: #f87171; }
  </style>
</head>
<body>

  <!-- Top Academic Credentials Bar -->
  <div class="top-bar">
    <div>
      🎓 <strong>CineSeat · Python DSA Academic Project</strong> | Evaluator: <strong>Mr. Vivek</strong>
    </div>
    <div>
      Student: <strong>Khushi</strong> | Reg No: <strong>251302194</strong> | Stack: <strong>Pure Python 3.14 + Flask</strong>
    </div>
  </div>

  <!-- Header -->
  <header>
    <div class="brand">
      <div class="brand-logo">CineSeat</div>
      <div class="brand-tag">Python DSA Engine v2.0</div>
    </div>
    <div class="nav-links">
      <button class="nav-btn active" onclick="switchTab('browse')">🎬 Movies</button>
      <button class="nav-btn" onclick="switchTab('my-tickets')">🎟️ My Tickets</button>
      <button class="nav-btn" onclick="switchTab('theatres')">📍 NCR Theatres (Dijkstra)</button>
      <button class="nav-btn" onclick="switchTab('dsa')">⚡ DSA Architecture & Live Inspector</button>
    </div>
  </header>

  <main id="main-content">
    <!-- Browse Tab -->
    <div id="tab-browse">
      <section class="filter-section">
        <div class="search-box">
          <input type="text" id="search-input" placeholder="Search 56 movies (Trie Prefix Engine)..." oninput="handleSearch()">
          <div class="search-hint">💡 Powered by <strong>MovieTrie</strong> (Prefix tree with O(L) lookup complexity)</div>
        </div>
        <div class="control-group">
          <select id="genre-select" onchange="loadMovies()">
            <option value="All">All Genres</option>
            <option value="Action">Action</option>
            <option value="Drama">Drama</option>
            <option value="Sci-Fi">Sci-Fi</option>
            <option value="Comedy">Comedy</option>
            <option value="Thriller">Thriller</option>
          </select>
          <select id="sort-select" onchange="loadMovies()">
            <option value="rating">Top Rated (Merge Sort O(N log N))</option>
            <option value="price">Price: Low to High (Quick Sort O(N log N))</option>
            <option value="hype">Popularity Hype (Quick Sort)</option>
            <option value="name">Alphabetical (Merge Sort)</option>
          </select>
        </div>
      </section>

      <div class="movie-grid" id="movie-grid">
        <!-- Rendered dynamically -->
      </div>
    </div>

    <!-- My Tickets Tab -->
    <div id="tab-my-tickets" style="display: none;">
      <h2 style="margin-bottom: 16px; color: var(--accent);">Your Confirmed Bookings & Receipts</h2>
      <p style="color: var(--muted); margin-bottom: 24px;">
        Cancellations trigger <strong>BookingHistoryStack (LIFO)</strong> rollback and immediately reallocate freed seats via <strong>FIFO Queue</strong>.
      </p>
      <div id="tickets-container">
        <!-- Rendered dynamically -->
      </div>
    </div>

    <!-- Theatres & Dijkstra Tab -->
    <div id="tab-theatres" style="display: none;">
      <h2 style="margin-bottom: 16px; color: var(--accent);">Delhi NCR Theatres & Road Routing</h2>
      <p style="color: var(--muted); margin-bottom: 20px;">
        Shortest route calculated using <strong>Dijkstra's Algorithm (O((V + E) log V))</strong> on weighted NCR graph network.
      </p>
      <div style="background: var(--card-bg); padding: 20px; border-radius: 12px; border: 1px solid var(--border); margin-bottom: 24px; display: flex; gap: 16px; align-items: center;">
        <label>Your Starting Location:</label>
        <select id="user-location-select" onchange="loadNearestTheatre()">
          <option value="Connaught Place">Connaught Place (Central)</option>
          <option value="Karol Bagh" selected>Karol Bagh (West/Central)</option>
          <option value="Saket">Saket (South Delhi)</option>
          <option value="Nehru Place">Nehru Place (South)</option>
          <option value="Cyber City">Cyber City (Gurgaon)</option>
          <option value="Noida Sector 18">Noida Sector 18 (East)</option>
        </select>
      </div>
      <div id="theatre-routing-result"></div>
    </div>

    <!-- DSA Diagnostics Tab -->
    <div id="tab-dsa" style="display: none;">
      <h2 style="margin-bottom: 16px; color: var(--accent);">Data Structures & Algorithms (DSA) Live Visualizer</h2>
      <p style="color: var(--muted); margin-bottom: 24px;">
        Comprehensive academic proof for Faculty Evaluator <strong>Mr. Vivek</strong>.
      </p>
      <div id="dsa-dashboard"></div>
    </div>
  </main>

  <!-- Seat Booking Modal -->
  <div class="modal-overlay" id="booking-modal">
    <div class="modal-content">
      <button class="modal-close" onclick="closeModal('booking-modal')">&times;</button>
      <h2 id="modal-movie-title" style="margin-bottom: 8px; color: var(--accent);">Select Experience & Seats</h2>
      <p id="modal-movie-meta" style="color: var(--muted); margin-bottom: 20px;"></p>

      <div style="display: flex; gap: 12px; margin-bottom: 20px;">
        <select id="show-select" style="flex: 1;" onchange="loadSeatGrid()"></select>
      </div>

      <div style="background: var(--surface); padding: 12px 16px; border-radius: 8px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center;">
        <span>Adjacent Recliner Suggestion:</span>
        <button class="btn btn-secondary" style="flex: initial;" onclick="autoSuggestSeats()">✨ Suggest 2 Recliners (Sliding Window)</button>
      </div>

      <div class="seat-screen">CINEMA SCREEN THIS WAY</div>
      <div class="seat-grid" id="modal-seat-grid"></div>

      <div class="seat-legend">
        <div class="legend-item"><div class="legend-color" style="background: var(--surface);"></div> Available</div>
        <div class="legend-item"><div class="legend-color" style="background: var(--accent);"></div> Selected</div>
        <div class="legend-item"><div class="legend-color" style="background: var(--booked);"></div> Booked</div>
        <div class="legend-item"><div class="legend-color" style="border: 2px dashed var(--accent);"></div> Suggested</div>
      </div>

      <div style="background: var(--surface); padding: 16px; border-radius: 8px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
          <span>Selected Seats: <strong id="selected-seats-label">None</strong></span>
          <span>Seat Subtotal: <strong id="selected-seats-price">₹0</strong></span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <span>Snacks Combo (₹180/ea):</span>
          <input type="number" id="snacks-input" min="0" max="10" value="0" style="width: 60px; padding: 4px;" onchange="updateTotal()">
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>Promo Code:</span>
          <input type="text" id="promo-input" placeholder="Try MOVIENIGHT" style="padding: 4px 8px; width: 140px; text-transform: uppercase;" oninput="updateTotal()">
        </div>
        <hr style="border-color: var(--border); margin: 12px 0;">
        <div style="display: flex; justify-content: space-between; font-size: 18px; font-weight: 800; color: var(--accent);">
          <span>Grand Total:</span>
          <span id="grand-total-label">₹0</span>
        </div>
      </div>

      <div style="display: flex; gap: 12px;">
        <select id="payment-mode-select" style="flex: 1;">
          <option value="UPI">UPI (Google Pay / PhonePe)</option>
          <option value="Card">Credit / Debit Card</option>
          <option value="Cash">Cash at Counter</option>
        </select>
        <button class="btn btn-primary" style="flex: 2;" onclick="confirmBooking()">Confirm & Generate Ticket</button>
      </div>
    </div>
  </div>

  <!-- Ticket Receipt Modal -->
  <div class="modal-overlay" id="receipt-modal">
    <div class="modal-content" style="max-width: 520px; text-align: center;">
      <button class="modal-close" onclick="closeModal('receipt-modal')">&times;</button>
      <div style="font-size: 40px; margin-bottom: 12px;">🎟️</div>
      <h2 style="color: var(--accent); margin-bottom: 6px;">Booking Confirmed!</h2>
      <p style="color: var(--muted); font-size: 13px; margin-bottom: 20px;">Simulated Digital Admission Pass</p>

      <div id="receipt-details" style="background: var(--surface); border: 1px dashed var(--accent); border-radius: 12px; padding: 20px; text-align: left; font-size: 14px; margin-bottom: 20px;"></div>

      <div style="display: flex; gap: 10px;">
        <button class="btn btn-primary" onclick="window.print()">🖨️ Print Ticket / Receipt</button>
        <button class="btn btn-secondary" onclick="closeModal('receipt-modal'); switchTab('my-tickets');">View All Tickets</button>
      </div>
    </div>
  </div>

  <script>
    let currentMovies = [];
    let selectedSeats = new Set();
    let currentShowData = null;
    let selectedMovie = null;

    // Switch Tabs
    function switchTab(tab) {
      document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
      document.getElementById('tab-browse').style.display = 'none';
      document.getElementById('tab-my-tickets').style.display = 'none';
      document.getElementById('tab-theatres').style.display = 'none';
      document.getElementById('tab-dsa').style.display = 'none';

      if (tab === 'browse') {
        document.getElementById('tab-browse').style.display = 'block';
        event?.target?.classList.add('active');
      } else if (tab === 'my-tickets') {
        document.getElementById('tab-my-tickets').style.display = 'block';
        loadMyTickets();
      } else if (tab === 'theatres') {
        document.getElementById('tab-theatres').style.display = 'block';
        loadNearestTheatre();
      } else if (tab === 'dsa') {
        document.getElementById('tab-dsa').style.display = 'block';
        loadDsaDiagnostics();
      }
    }

    // Load Movies with Trie or Sort
    async function loadMovies() {
      const q = document.getElementById('search-input').value.trim();
      const genre = document.getElementById('genre-select').value;
      const sortBy = document.getElementById('sort-select').value;

      const url = `/api/movies?query=${encodeURIComponent(q)}&genre=${encodeURIComponent(genre)}&sortBy=${sortBy}`;
      const res = await fetch(url);
      const data = await res.json();
      currentMovies = data.movies;
      renderMovieGrid(currentMovies);
    }

    let searchTimeout;
    function handleSearch() {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(loadMovies, 150);
    }

    function renderMovieGrid(movies) {
      const grid = document.getElementById('movie-grid');
      grid.innerHTML = '';
      if (!movies || movies.length === 0) {
        grid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--muted); padding: 40px;">No movies matched your search query in MovieTrie.</p>';
        return;
      }

      movies.forEach(m => {
        const card = document.createElement('div');
        card.className = 'movie-card';
        card.innerHTML = `
          <div class="poster-box">
            <img src="${m.poster}" alt="${m.name}" onerror="this.src='https://placehold.co/300x450/1a2717/c7e998?text=${encodeURIComponent(m.name)}'">
            <div class="poster-badge">⭐ ${m.rating} / 10</div>
          </div>
          <div class="card-body">
            <div class="movie-title">${m.name}</div>
            <div class="movie-meta">${m.genre} · ${m.duration} mins · ${m.language}</div>
            <div class="movie-synopsis">${m.synopsis}</div>
            <div class="card-actions">
              <button class="btn btn-primary" onclick="openBookingModal(${m.id})">Book Tickets (₹${m.price})</button>
            </div>
          </div>
        `;
        grid.appendChild(card);
      });
    }

    // Booking Modal
    async function openBookingModal(movieId) {
      selectedMovie = currentMovies.find(m => m.id === movieId);
      if (!selectedMovie) return;

      document.getElementById('modal-movie-title').textContent = `${selectedMovie.name} (${selectedMovie.year})`;
      document.getElementById('modal-movie-meta').textContent = `${selectedMovie.genre} · Directed by ${selectedMovie.director} · Starring ${selectedMovie.cast}`;

      // Fetch shows for today
      const res = await fetch(`/api/shows?movieId=${movieId}&date=2026-10-31`);
      const shows = await res.json();

      const showSelect = document.getElementById('show-select');
      showSelect.innerHTML = '';
      shows.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s.id;
        opt.textContent = `${s.theatreName} (${s.area}) · ${s.time} · ${s.format} (${s.projection}) · ${s.availableSeats} seats left`;
        showSelect.appendChild(opt);
      });

      document.getElementById('booking-modal').classList.add('open');
      selectedSeats.clear();
      await loadSeatGrid();
    }

    async function loadSeatGrid() {
      const showKey = document.getElementById('show-select').value;
      if (!showKey) return;

      const res = await fetch(`/api/seats?showKey=${encodeURIComponent(showKey)}`);
      currentShowData = await res.json();

      renderSeatGrid(currentShowData.grid);
      updateTotal();
    }

    function renderSeatGrid(grid) {
      const container = document.getElementById('modal-seat-grid');
      container.innerHTML = '';

      grid.forEach(row => {
        row.forEach(seat => {
          const cell = document.createElement('div');
          cell.className = `seat-cell ${seat.status === 'Booked' ? 'booked' : ''} ${selectedSeats.has(seat.label) ? 'selected' : ''}`;
          cell.id = `seat-${seat.label}`;
          cell.innerHTML = `<div>${seat.label}</div><div style="font-size: 10px; font-weight: normal; opacity: 0.8;">₹${seat.price}</div>`;

          if (seat.status !== 'Booked') {
            cell.onclick = () => toggleSeat(seat.label);
          }
          container.appendChild(cell);
        });
      });
    }

    function toggleSeat(label) {
      if (selectedSeats.has(label)) {
        selectedSeats.delete(label);
      } else {
        if (selectedSeats.size >= 8) {
          alert("Maximum 8 seats allowed per performance.");
          return;
        }
        selectedSeats.add(label);
      }
      renderSeatGrid(currentShowData.grid);
      updateTotal();
    }

    async function autoSuggestSeats() {
      const showKey = document.getElementById('show-select').value;
      const res = await fetch(`/api/suggest-seats?showKey=${encodeURIComponent(showKey)}&count=2&tier=Recliner`);
      const data = await res.json();
      if (data.suggestedSeats && data.suggestedSeats.length > 0) {
        selectedSeats.clear();
        data.suggestedSeats.forEach(s => selectedSeats.add(s));
        renderSeatGrid(currentShowData.grid);
        updateTotal();
      } else {
        alert("No 2 adjacent Recliner seats currently free in this performance.");
      }
    }

    function updateTotal() {
      let subtotal = 0;
      if (currentShowData && currentShowData.grid) {
        currentShowData.grid.forEach(row => {
          row.forEach(seat => {
            if (selectedSeats.has(seat.label)) {
              subtotal += seat.price;
            }
          });
        });
      }

      const snacks = parseInt(document.getElementById('snacks-input').value) || 0;
      const snackCost = snacks * 180;
      const promo = document.getElementById('promo-input').value.trim().toUpperCase();
      const discount = promo === 'MOVIENIGHT' ? Math.round(subtotal * 0.10) : 0;
      const grandTotal = Math.max(0, subtotal - discount + snackCost);

      document.getElementById('selected-seats-label').textContent = Array.from(selectedSeats).join(', ') || 'None';
      document.getElementById('selected-seats-price').textContent = `₹${subtotal}`;
      document.getElementById('grand-total-label').textContent = `₹${grandTotal} ${discount > 0 ? '(10% Off Applied)' : ''}`;
    }

    async function confirmBooking() {
      if (selectedSeats.size === 0) {
        alert("Please select at least one seat.");
        return;
      }

      const showKey = document.getElementById('show-select').value;
      const snacks = parseInt(document.getElementById('snacks-input').value) || 0;
      const promo = document.getElementById('promo-input').value.trim();
      const mode = document.getElementById('payment-mode-select').value;

      const payload = {
        items: [{ showKey: showKey, seats: Array.from(selectedSeats) }],
        snacks: snacks,
        promo: promo,
        mode: mode
      };

      const res = await fetch('/api/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();

      if (data.success) {
        closeModal('booking-modal');
        showReceipt(data.order);
      } else {
        alert(`Booking Error: ${data.error}`);
      }
    }

    function showReceipt(order) {
      const b = order.bookings[0];
      const html = `
        <div style="font-weight: 800; font-size: 18px; margin-bottom: 8px;">${b.title}</div>
        <div style="color: var(--accent); margin-bottom: 12px;">${b.theatreName} · ${b.screen} (${b.format})</div>
        <div style="margin-bottom: 6px;"><strong>Date & Time:</strong> ${b.date} at ${b.time}</div>
        <div style="margin-bottom: 6px;"><strong>Seats:</strong> <span style="color: var(--accent); font-weight: 700;">${b.seats.join(', ')}</span></div>
        <div style="margin-bottom: 6px;"><strong>Order ID:</strong> #${order.orderId} | <strong>Ticket ID:</strong> TICKET-${b.id}</div>
        <div style="margin-bottom: 6px;"><strong>Paid Amount:</strong> ₹${order.grandTotal} (${order.mode})</div>
        <div style="margin-top: 14px; padding: 10px; background: #10190f; text-align: center; font-family: monospace; letter-spacing: 4px; border-radius: 6px;">
          ||| | |||| | |||||| || | |||| ||
          <div style="font-size: 11px; letter-spacing: 1px; color: var(--muted); margin-top: 4px;">CINESEAT-TOKEN-${b.id}</div>
        </div>
      `;
      document.getElementById('receipt-details').innerHTML = html;
      document.getElementById('receipt-modal').classList.add('open');
    }

    // Load My Tickets
    async function loadMyTickets() {
      const res = await fetch('/api/my-bookings');
      const bookings = await res.json();
      const container = document.getElementById('tickets-container');
      container.innerHTML = '';

      if (!bookings || bookings.length === 0) {
        container.innerHTML = '<p style="color: var(--muted); padding: 40px; text-align: center;">No tickets booked yet. Book a movie above!</p>';
        return;
      }

      bookings.forEach(b => {
        const div = document.createElement('div');
        div.style = "background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center;";
        const isCancelled = b.status === 'Cancelled';
        div.innerHTML = `
          <div>
            <div style="font-size: 18px; font-weight: 700;">${b.title} <span class="badge ${isCancelled ? 'badge-danger' : 'badge-success'}">${b.status}</span></div>
            <div style="color: var(--muted); font-size: 13px; margin: 4px 0;">${b.theatreName} · ${b.date} at ${b.time} (${b.format})</div>
            <div>Seats: <strong>${b.seats.join(', ')}</strong> | Paid: <strong>₹${b.price}</strong> (${b.mode})</div>
            <div style="font-size: 12px; color: var(--muted); margin-top: 4px;">Ticket Code: TICKET-${b.id}</div>
          </div>
          <div>
            ${!isCancelled ? `<button class="btn btn-secondary" style="background: #4d2020; border-color: #6b2a2a; color: #ff9999;" onclick="cancelBooking(${b.id})">Cancel Ticket</button>` : '<span style="color: var(--muted); font-size: 13px;">Refund Processed</span>'}
          </div>
        `;
        container.appendChild(div);
      });
    }

    async function cancelBooking(bookingId) {
      if (!confirm("Are you sure you want to cancel this booking? Freed seats will be reallocated to the earliest waiting list group.")) return;
      const res = await fetch('/api/cancel-booking', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bookingId: bookingId })
      });
      const data = await res.json();
      if (data.success) {
        alert(`Booking #${bookingId} Cancelled. Refund Amount: ₹${data.refundAmount}`);
        loadMyTickets();
      } else {
        alert(`Error: ${data.error}`);
      }
    }

    // Load Nearest Theatre via Dijkstra
    async function loadNearestTheatre() {
      const hub = document.getElementById('user-location-select').value;
      const res = await fetch(`/api/theatres/nearest?hub=${encodeURIComponent(hub)}`);
      const data = await res.json();

      let venuesHtml = data.allVenues.map(v => `
        <div style="background: var(--card-bg); border: 1px solid var(--border); border-radius: 10px; padding: 16px; margin-bottom: 12px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <strong style="font-size: 16px; color: var(--accent);">${v.theatreName} (${v.area})</strong>
            <span class="badge badge-success">${v.distanceKm} km · ~${v.travelMinutes} mins</span>
          </div>
          <div style="font-size: 13px; color: var(--muted); margin-bottom: 6px;">Optimal Route: <strong>${v.route.join(' ➔ ')}</strong></div>
        </div>
      `).join('');

      document.getElementById('theatre-routing-result').innerHTML = `
        <div style="margin-bottom: 20px;">
          <h3 style="color: var(--accent); margin-bottom: 8px;">🌟 Nearest Multiplex: ${data.nearest.theatreName}</h3>
          <p style="color: var(--muted);">Direct shortest distance: <strong>${data.nearest.distanceKm} km</strong> | Travel time: ~<strong>${data.nearest.travelMinutes} minutes</strong></p>
        </div>
        ${venuesHtml}
      `;
    }

    // Load DSA Diagnostics
    async function loadDsaDiagnostics() {
      const res = await fetch('/api/dsa-diagnostics');
      const diag = await res.json();
      const div = document.getElementById('dsa-dashboard');

      div.innerHTML = `
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px;">
          <div style="background: var(--card-bg); border: 1px solid var(--border); padding: 18px; border-radius: 12px;">
            <h3 style="color: var(--accent); margin-bottom: 8px;">1. MovieTrie (Prefix Tree)</h3>
            <p style="font-size: 13px; color: var(--muted); margin-bottom: 10px;">Sub-millisecond title prefix search and autocomplete.</p>
            <div>• Indexed Words: <strong>${diag.movieTrie.totalIndexedWords}</strong></div>
            <div>• Root Branches: <strong>${diag.movieTrie.rootChildBranches}</strong></div>
            <div>• Time Complexity: <strong>${diag.movieTrie.lookupComplexity}</strong></div>
          </div>

          <div style="background: var(--card-bg); border: 1px solid var(--border); padding: 18px; border-radius: 12px;">
            <h3 style="color: var(--accent); margin-bottom: 8px;">2. MovieBST (Binary Search Tree)</h3>
            <p style="font-size: 13px; color: var(--muted); margin-bottom: 10px;">Numerical indexing for movie ratings & range queries.</p>
            <div>• Total Tree Nodes: <strong>${diag.ratingBST.totalNodes}</strong></div>
            <div>• Rating Bounds: <strong>${diag.ratingBST.minRating} ⭐ to ${diag.ratingBST.maxRating} ⭐</strong></div>
            <div>• Range Query Complexity: <strong>${diag.ratingBST.rangeQueryComplexity}</strong></div>
          </div>

          <div style="background: var(--card-bg); border: 1px solid var(--border); padding: 18px; border-radius: 12px;">
            <h3 style="color: var(--accent); margin-bottom: 8px;">3. 2D Seat Matrix & Sliding Window</h3>
            <p style="font-size: 13px; color: var(--muted); margin-bottom: 10px;">8x5 hall grid with adjacent seat spatial scoring.</p>
            <div>• Active Show Matrices: <strong>${diag.seatMatricesActive}</strong></div>
            <div>• Adjacent Recommendation: <strong>Sliding Window O(R * C)</strong></div>
            <div>• Center-Screen Weighting: <strong>Minimizes Viewing Distance</strong></div>
          </div>

          <div style="background: var(--card-bg); border: 1px solid var(--border); padding: 18px; border-radius: 12px;">
            <h3 style="color: var(--accent); margin-bottom: 8px;">4. TheatreGraph & Dijkstra</h3>
            <p style="font-size: 13px; color: var(--muted); margin-bottom: 10px;">Weighted road network of Delhi NCR cinemas.</p>
            <div>• Urban Hub Nodes: <strong>${diag.theatreGraph.totalHubs}</strong></div>
            <div>• Connected Multiplexes: <strong>${diag.theatreGraph.venuesConnected}</strong></div>
            <div>• Complexity: <strong>${diag.theatreGraph.algorithm}</strong></div>
          </div>

          <div style="background: var(--card-bg); border: 1px solid var(--border); padding: 18px; border-radius: 12px;">
            <h3 style="color: var(--accent); margin-bottom: 8px;">5. BookingHistoryStack (LIFO)</h3>
            <p style="font-size: 13px; color: var(--muted); margin-bottom: 10px;">Rollback, undo and audit tracking for bookings.</p>
            <div>• Stack Size: <strong>${diag.historyStackSize} recorded events</strong></div>
            <div>• Push / Pop Complexity: <strong>O(1)</strong></div>
          </div>

          <div style="background: var(--card-bg); border: 1px solid var(--border); padding: 18px; border-radius: 12px;">
            <h3 style="color: var(--accent); margin-bottom: 8px;">6. CustomHashTable (Separate Chaining)</h3>
            <p style="font-size: 13px; color: var(--muted); margin-bottom: 10px;">Instant digital ticket lookup and verification.</p>
            <div>• Capacity / Stored: <strong>${diag.ticketHashTable.capacity} buckets / ${diag.ticketHashTable.storedTickets} tickets</strong></div>
            <div>• Load Factor: <strong>${diag.ticketHashTable.loadFactor}</strong></div>
            <div>• Verification Complexity: <strong>${diag.ticketHashTable.lookupComplexity}</strong></div>
          </div>
        </div>
      `;
    }

    function closeModal(id) {
      document.getElementById(id).classList.remove('open');
    }

    // Initial Load
    loadMovies();
  </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(INDEX_HTML)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"================================================================")
    print(f" CineSeat Python DSA Web Application Started")
    print(f" Student: Khushi (Reg No: 251302194) | Faculty: Mr. Vivek")
    print(f" Server running at: http://127.0.0.1:{port}")
    print(f"================================================================")
    app.run(host="0.0.0.0", port=port, debug=False)
