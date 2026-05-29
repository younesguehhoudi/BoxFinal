# Technical Documentation — Travel Planner

## 1. Architecture

We chose a 3-layer architecture to keep responsibilities separated :

- data: database connection and table definitions
- logic : algo logic (auth, places, tours, algorithm)
- ui : console menus and user interaction

## 2. Technology choices

- Python : all team members are comfortable with it
- SQLite : lightweight, no server needed, sufficient for this project
- geopy (Nominatim) : free geocoding API, no key required

## 3. Algorithm — Tour Optimization

### Problem

We need to visit all places once and return to the start, minimizing distance.
Brute force is O(n!), unusable beyond ~12 places, so we use heuristics.

https://en.wikipedia.org/wiki/Travelling_salesman_problem

### Step 1 — Multi-start Nearest Neighbor

We run Nearest Neighbor from every place as starting point and keep the best result.
This removes the dependency on a single starting point, which is the main weakness
of basic Nearest Neighbor.

Complexity : O(n³). Fine for datasets under 50 places.

https://en.wikipedia.org/wiki/Nearest_neighbour_algorithm

### Step 2 — 2-opt improvement

We apply 2-opt on top of the Nearest Neighbor result. It checks every pair of
segments and reverses the one between them if it shortens the tour.
Repeated until no improvement is found. Removes crossing segments.

Complexity : O(n²) per iteration.

https://en.wikipedia.org/wiki/2-opt

### Why this approach

The combination of multi-start Nearest Neighbor and 2-opt is a well-known
and solid approach for the TSP. It's simple to implement, easy to justify,
and gives good results for small datasets.

---

## 4. Algorithm — Hotel Planning (K-Means)

Complexity 
O(n × k × i)
n is number of places
and k number of hotels 
### Problem

After generating a tour, the user can choose to add hotels.
We group nearby cities into clusters and assign one hotel per cluster
(the most central city). The tour then connects hotels instead of all cities.
Non-hotel cities require a round trip from their hotel.

Total distance = hotel tour + Σ round trips to non-hotel cities.

### K-Means implementation

We implemented K-Means from scratch (no sklearn).

Each iteration assigns every place to its nearest hotel, then recomputes
each cluster's center and picks the closest real place as the new hotel.
Stops when assignments no longer change.

### Choosing k

Two modes are available :

- Optimal : tests all k values, picks the one with lowest total distance.
  Can return k = n (one hotel per city) which is unrealistic.
- Compromise : increases k only while improvement exceeds 5%.
  Gives a realistic number of hotels.

The user sees optimal first, then compromise if rejected.

### Why this approach

K-Means is a simple and well-established clustering algorithm.
Our hotel selection (closest to centroid) minimizes intra-cluster travel.
The two k-selection modes give the user a meaningful choice.