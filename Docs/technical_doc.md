# Technical Documentation — Travel Planner

## 1. Architecture

We chose a 3-layer architecture to keep responsibilities separated :

- data: database connection and table definitions
- logic : algo logic (auth, places, tours, algorithm)
- ui : console menus and user interaction

## 2. Technology choices

- Python : all team members are comfortable with it
- SQLite : lightweight, no server needed, sufficient for this project

## 3. Algorithm 

## Algorithm — Tour Optimization

### Problem

The subject requires visiting all places exactly once and returning 
to the starting point, minimizing the total distance.

An exact solution is not feasible : the number of possible tours 
grows as n!, making it computationally impossible beyond ~15 places.
We therefore use a heuristic approach.

https://en.wikipedia.org/wiki/Travelling_salesman_problem


### Step 1 — Multi-start Nearest Neighbor

The classic Nearest Neighbor algorithm starts from one place and 
always moves to the closest unvisited place.

Its main weakness : a bad starting point can produce a poor tour.

Our improvement : we run Nearest Neighbor from every place as a 
starting point, then keep the tour with the lowest total distance.

Complexity : O(n³) — n times O(n²).
Acceptable for the expected dataset size (under 50 places), for tour planning it seems reasonable.
https://en.wikipedia.org/wiki/Nearest_neighbour_algorithm
https://grokipedia.com/page/Nearest_neighbour_algorithm

### Step 2 — 2-opt improvement

2-opt is a local search algorithm applied on top of the 
Nearest Neighbor result.

It iterates over every pair of segments in the tour and checks 
if reversing the segment between them produces a shorter tour.
If yes, the reversal is kept. The process repeats until no 
improvement is found.

A tour with crossing segments is always longer than the same tour 
without crossings. 2-opt systematically removes these crossings.

Complexity : O(n²) per iteration, repeated until convergence.
https://en.wikipedia.org/wiki/2-opt

### Why this approach

- Exceeds naive and random solutions as required by the subject
- Multi-start removes the dependency on a single starting point,
  which is the main weakness of basic Nearest Neighbor
- 2-opt significantly improves the initial tour quality
- Both algorithms are simple to implement, test and maintain
- The combination gives near-optimal results for small datasets

### Considered alternatives

- Basic Nearest Neighbor : faster but starting-point dependent
- Random + 2-opt : excluded, random is forbided by the subject
- Exact brute force : O(n!), unusable beyond 12-15 places