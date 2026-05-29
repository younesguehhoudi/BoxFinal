# Database Documentation — Travel Planner

**Authors:** Abdallah Alamoush · Younes Guehhoudi · Noé Loisel

---

## Overview

The project uses **SQLite** as its database. SQLite is a lightweight, file-based database — no server, no configuration, nothing to install. The entire database lives in a single file called `travel_planner.db` at the root of the project.

The database is created automatically the first time you run `main.py`. You do not need to set anything up manually.

---

## Connection

All database access goes through a single function in `Data/DataBase.py`:

```python
import sqlite3

DATABASE_NAME = "travel_planner.db"

def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection
```

`row_factory = sqlite3.Row` makes query results accessible by column name (e.g. `row["username"]`) instead of by index. Every file that needs the database imports and calls this function.

---

## Tables

The tables are defined and created in `Data/Models.py`. The function `initialize_database()` is called once at startup from `main.py`.

### users

Stores registered accounts.

```sql
CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT NOT NULL UNIQUE,
    password    TEXT NOT NULL,
    created_at  TEXT DEFAULT CURRENT_TIMESTAMP
);
```

| Column | Description |
|---|---|
| id | Auto-incremented unique identifier |
| username | Must be unique — login name |
| password | Hashed with PBKDF2-SHA256 via Werkzeug, never stored in plain text |
| created_at | Timestamp set automatically on insert |

---

### places

Stores cities added by each user.

```sql
CREATE TABLE IF NOT EXISTS places (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    name        TEXT NOT NULL,
    latitude    REAL NOT NULL,
    longitude   REAL NOT NULL,
    created_at  TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

| Column | Description |
|---|---|
| id | Auto-incremented unique identifier |
| user_id | Links the place to its owner |
| name | City name entered by the user |
| latitude / longitude | Fetched automatically via geopy (Nominatim) |
| created_at | Timestamp set automatically on insert |

`ON DELETE CASCADE` means if a user is deleted, all their places are deleted too.

---

### tours

Stores generated and saved tours.

```sql
CREATE TABLE IF NOT EXISTS tours (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    name            TEXT NOT NULL,
    total_distance  REAL NOT NULL,
    visibility      TEXT NOT NULL CHECK(visibility IN ('public', 'private')),
    share_token     TEXT NOT NULL UNIQUE,
    created_at      TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

| Column | Description |
|---|---|
| id | Auto-incremented unique identifier |
| user_id | Links the tour to its creator |
| name | Name given to the tour by the user |
| total_distance | Total distance in km, calculated at generation time |
| visibility | Either `public` or `private` — enforced by a CHECK constraint |
| share_token | UUID generated automatically, used to share the tour |
| created_at | Timestamp set automatically on insert |

`ON DELETE CASCADE` means if a user is deleted, all their tours are deleted too.

---

### tour_places

Junction table that links tours to their places, in order.

```sql
CREATE TABLE IF NOT EXISTS tour_places (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    tour_id   INTEGER NOT NULL,
    place_id  INTEGER NOT NULL,
    position  INTEGER NOT NULL,
    FOREIGN KEY (tour_id)  REFERENCES tours(id)  ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE
);
```

| Column | Description |
|---|---|
| tour_id | References the tour |
| place_id | References the place |
| position | The order of the place in the tour (0, 1, 2 ...) |

When a tour is loaded, places are fetched ordered by `position` to reconstruct the route in the right order.

---

## Entity-Relationship Diagram

```
users
 id ──────────────────────────────────────┐
 username                                 │
 password                                 │
 created_at                               │
                                          │ 1
                              ┌───────────┴──────────┐
                              │                      │
                           places                  tours
                            id ◄──────────┐         id ◄──────────┐
                            user_id       │         user_id        │
                            name          │         name           │
                            latitude      │         total_distance │
                            longitude     │         visibility     │
                            created_at    │         share_token    │
                                          │         created_at     │
                                          │                        │
                                     tour_places                   │
                                      id                           │
                                      tour_id ──────────────────────┘
                                      place_id ──────────┘
                                      position
```

---

## Known Limitations & Workflow

### Current situation

The project uses SQLite, a local file-based database (`travel_planner.db`). This means each team member has their own database on their machine. SQLite files are binary and cannot be merged by Git — any conflict must be resolved manually by choosing one version over the other.

### Team workflow to share database changes

To push your database to the team:

```bash
git add travel_planner.db
git commit -m "chore: update database"
git push
```

To pull the latest database from the team:

```bash
del travel_planner.db        # Windows
rm travel_planner.db         # Linux/Mac
git pull
```

Always delete your local database before pulling, otherwise Git will raise a binary conflict and the pull will fail.

### Known limitation

This workflow is manual and error-prone. It does not allow real-time data sharing — if two members modify the database simultaneously, one version will be lost.

### Improvement path

Migrating to a shared online database (e.g. Supabase + PostgreSQL) would solve all of these issues. The `get_connection()` function in `Data/DataBase.py` is the only entry point for database access — replacing it with a PostgreSQL connection would require minimal changes to the rest of the codebase (`?` → `%s` for query placeholders, `lastrowid` → `RETURNING id`).