# Travel Planner

## Overview
Travel Planner is a console-based Python application designed to optimize travel itineraries. It allows users to securely manage their accounts, save geographical places using real-world coordinates, and generate optimal travel routes. The application employs advanced heuristics (Multi-start Nearest Neighbor and 2-opt) to minimize travel distance and offers an intelligent hotel planning feature using K-Means clustering.

This project was developed as part of the Licence 3 Sciences du Numérique final certification.

## Features
*   **User Authentication:** Secure account creation and login system using `pbkdf2:sha256` password hashing. Data is strictly isolated per user.
*   **Place Management:** Add points of interest by name. The application automatically fetches precise geographical coordinates (latitude/longitude) using the Geopy Nominatim API.
*   **Tour Optimization:** Solves the Travelling Salesman Problem (TSP) using a Multi-start Nearest Neighbor algorithm, further optimized by a 2-opt local search to guarantee the shortest possible round-trip distance.
*   **Hotel Planning (Clustering):** Automatically groups nearby places into clusters and designates a central 'Hotel' for each using a custom K-Means implementation. Calculates optimal round-trip distances from hotels to assigned cities.
*   **Tour Sharing:** Save tours with public or private visibility. Each saved tour generates a unique UUID share token, allowing sharing with other users (with access control for private tours).

## Architecture
The application follows a strict 3-layer architecture to ensure modularity and maintainability:
1.  **Data Layer (`Data/`):** Manages SQLite3 database connections and schema initialization (`travel_planner.db`).
2.  **Logic Layer (`Logic/`):** Contains the core business logic, including algorithmic computations, API calls, and object models (`Auth`, `Place`, `Tour`, `Algo`, `HotelPlanner`, `TourManager`).
3.  **UI Layer (`Ui/`):** Handles all user interactions via a modular Console/CLI interface (`ConsoleMenu`, `Login`, `TourPrinter`, etc.).

## Installation

### Prerequisites
*   Python 3.10+
*   `pip` package manager

### Setup
1. Clone the repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
*(Dependencies include `geopy` and `Werkzeug`)*

3. Start the application:
   ```bash
   python main.py
   ```
The SQLite database (`travel_planner.db`) will be initialized automatically on the first run.

## Database Sharing

This project uses a local SQLite database (`travel_planner.db`).
Since SQLite is a binary file, it cannot be merged by Git automatically.

### Workflow to share database changes with the team

**Before pushing changes to the database:**
```bash
git add travel_planner.db
git commit -m "chore: update database"
git push
```

**Before pulling when someone else updated the database:**
```bash
del travel_planner.db        # Windows
rm travel_planner.db         # Linux/Mac
git pull
```
The database will be replaced by the remote version.
If the file is not deleted before pulling, Git will raise a binary conflict.

## Usage Guide
Upon launching the application, you will be greeted by the Main Menu:

1.  **Login or create an account:** You must be authenticated to add places or generate personalized tours.
2.  **Add a place:** Type the name of a city or location (e.g., "Paris", "Tokyo"). The application will fetch its coordinates.
3.  **Display my places:** View all locations saved to your profile.
4.  **Generate and save a tour:** 
    *   Choose which places to include in your tour.
    *   The algorithm will compute the optimal route.
    *   You will be prompted to add hotels (Optimal vs Compromise clustering).
    *   Finally, you can save the tour as `Public` or `Private` and receive a share token.
5.  **Display public tours:** Browse all tours made public by other users.
6.  **My saved tours:** View your own saved tour history.
7.  **Access a shared tour:** Enter a specific UUID share token to view a shared route.

## Testing
The project includes a comprehensive suite of unit tests verifying core logic, algorithms, and database operations.

To run the tests, execute the scripts located in the `Test/` directory. For example, using standard `unittest`:
```bash
python -m unittest discover -s Test -p "Test*.py"
```
