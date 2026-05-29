# Travel Planner

A Python console application that lets users save places, generate optimized travel tours, plan hotels along the route, and share their tours with others — all from the terminal.

**Built by:** Abdallah Alamoush · Younes Guehhoudi · Noé Loisel

---

## What does this project do?

You give the app a list of cities. It figures out the **shortest route to visit all of them and come back to the start** — a classic problem called the *Travelling Salesman Problem*. On top of that, it can suggest **where to stay along the route** using a clustering algorithm. Tours can be saved, set to public or private, and shared with a unique link token.

---

## Features

| Feature | Description |
|---|---|
| Auth | Register and log in with a securely hashed password |
| Places | Add any city — coordinates are fetched automatically |
| Tour generation | Optimized route through all selected places |
| Hotel planning | Automatic hotel suggestions using K-Means clustering |
| Save & share | Save tours as public or private, share via a unique token |
| Public tours | Browse all public tours from every user |

---

## Project Structure

```
BoxFinal/
│
├── main.py                  # Entry point — starts the app
│
├── Data/
│   ├── DataBase.py          # SQLite connection
│   └── Models.py            # Table creation (users, places, tours)
│
├── Logic/
│   ├── Auth.py              # Register & login (hashed passwords)
│   ├── Place.py             # Place class + geocoding + DB queries
│   ├── Tour.py              # Tour class
│   ├── TourManager.py       # Save, retrieve, share tours
│   ├── Algo.py              # TSP algorithm (Nearest Neighbour + 2-opt)
│   └── HotelPlanner.py      # Hotel clustering (K-Means from scratch)
│
├── Ui/
│   ├── ConsoleMenu.py       # Main menu loop
│   ├── Login.py             # Login/register screen
│   ├── PlacePrinter.py      # Add & display places
│   ├── TourPrinter.py       # Generate & display tours
│   └── TourSharingPrinter.py # Save, list, and access shared tours
│
├── Test/
│   ├── Logic/               # Unit tests for Auth, Place, Algo, Hotel
│   └── Ui/                  # UI tests
│
├── Docs/
│   └── technical_doc.md     # Technical documentation
│
├── travel_planner.db        # SQLite database (auto-generated on first run)
└── requirements.txt
```

---

## Installation

### Prerequisites

- Python 3.10 or higher
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-repo/BoxFinal.git
cd BoxFinal

# 2. (Optional but recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python main.py
```

That's it. The database is created automatically on first launch.

---

## Dependencies

```
geopy>=2.4.1       # Geocoding — converts city names to coordinates
Werkzeug>=3.0.0    # Password hashing (pbkdf2:sha256)
```

No external database server needed. Everything is stored locally in `travel_planner.db`.

---

## How to use it

When you run the app, you'll see this menu:

```
=== MAIN MENU ===
1. Login or create an account
2. Add a place
3. Display my places
4. Generate and save a tour
5. Display public tours
6. My saved tours
7. Access a shared tour (via token)
8. Quit
```

**Typical workflow:**
1. **Option 1** — Create an account or log in
2. **Option 2** — Add a few cities (e.g. Paris, Lyon, Bordeaux)
3. **Option 4** — Generate your optimized tour, optionally add hotels, then save and share it
4. **Option 7** — Paste a token to view a tour someone shared with you

---

## How the algorithms work

### Tour optimization — Travelling Salesman Problem

The goal is to find the shortest route that visits every place exactly once and returns to the start.

Brute force (trying every possible order) is **O(n!)** — completely unusable beyond ~12 cities. We use two heuristics instead:

**Step 1 — Multi-Start Nearest Neighbour `O(n³)`**

The Nearest Neighbour algorithm works like this: start from a city, always go to the closest unvisited city next, until all cities are visited.

The catch is that the result depends heavily on which city you start from. To fix this, we run the algorithm from *every* city as the starting point and keep the best result.

**Step 2 — 2-opt improvement `O(n²)` per pass**

We then refine the tour by checking every pair of route segments. If swapping (reversing the path between two edges) reduces the total distance, we apply the swap. We repeat until no improvement is possible. This removes any "crossing" paths in the tour.

```
Before 2-opt:   A → C → B → D → A   (inefficient, crossing paths)
After  2-opt:   A → B → C → D → A   (shorter, no crossings)
```

---

### Hotel planning — K-Means clustering

After generating a tour, the user can choose to add hotels. Instead of staying in every city, we group nearby cities into clusters and place one hotel per cluster (the most central city).

The total distance becomes:
> **inter-hotel tour** + **round trips** from each hotel to its nearby cities

We implemented **K-Means from scratch** (no sklearn).

```
1. Divide places into k groups
2. For each group, pick the most central place as the hotel
3. Re-assign every place to its nearest hotel
4. Repeat until nothing changes
```

**Choosing how many hotels (k):**

| Mode | How it works |
|---|---|
| **Optimal** | Tests every possible k, picks the one with the lowest total distance (can suggest one hotel per city — not always realistic) |
| **Compromise** | Only increases k if it improves distance by more than 5% — gives a more practical number of hotels |

The app shows the optimal result first, then the compromise if the user wants an alternative.

---

## Database schema

```
users         → id, username, password (hashed), created_at
places        → id, user_id, name, latitude, longitude, created_at
tours         → id, user_id, name, total_distance, visibility, share_token, created_at
tour_places   → id, tour_id, place_id, position
```

All passwords are hashed with **PBKDF2-SHA256** via Werkzeug — plain-text passwords are never stored.

---

## Tour sharing

Every saved tour gets a **unique UUID token** generated automatically. This token can be shared with anyone.

- **Public tours** can be accessed by anyone with the token, even without an account.
- **Private tours** require the viewer to be logged in.

---

## Tests

Tests are in the `Test/` folder, organized by layer.

```bash
# Run all tests
python -m pytest Test/

# Run a specific test file
python -m pytest Test/Logic/TestAlgo.py
```

Test files cover: authentication, place management, tour algorithm, and hotel planning.

---


## License

This project was developed as part of a university course project at FGES — Université Catholique de Lille.
