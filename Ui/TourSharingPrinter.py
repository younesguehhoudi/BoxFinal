from Logic.TourManager import save_tour, get_tours_by_user, get_tour_by_token
from Logic.Tour import Tour
from Logic.Place import save_place


# ─── DISPLAY HELPERS ──────────────────────────────────────────────────────────

def display_share_token(token: str):
    """
    Print the share token and the two access instructions for the user to copy.
    """
    print("\n╔══════════════════════════════════════════════════════╗")
    print("║               TOUR SAVED & SHAREABLE                ║")
    print("╠══════════════════════════════════════════════════════╣")
    print(f"  Share token : {token}")
    print("  → Anyone with this token can view the tour")
    print("    by choosing 'Access a shared tour' in the menu")
    print("╚══════════════════════════════════════════════════════╝")


def display_tour_summary(meta: dict, index: int | None = None):
    """
    Print a one-line summary of a tour from its metadata dict.
    """
    prefix = f"{index}. " if index is not None else "  "
    visibility_icon = "[PUBLIC]" if meta["visibility"] == "public" else "[PRIVATE]"
    print(
        f"{prefix}{visibility_icon}  {meta['name']}  —  {meta['total_distance']:.1f} km"
        f"  ({meta['created_at'][:10]})"
    )


def display_full_tour(tour_data: dict):
    """
    Print the full details of a tour (name, places, distance, token).
    """
    print(f"\n══ Tour : {tour_data['name']} ══")
    print(f"   Visibility  : {tour_data['visibility'].upper()}")
    print(f"   Distance    : {tour_data['total_distance']:.1f} km")
    print(f"   Created     : {tour_data['created_at'][:10]}")
    print(f"   Share token : {tour_data['share_token']}")
    print("\n   Route :")
    places = tour_data["places"]
    for i, place in enumerate(places):
        arrow = "-> " if i < len(places) - 1 else "<- "
        print(f"     {arrow}{place.name} ({place.lat:.4f}, {place.lng:.4f})")
    print(f"     (back to {places[0].name})")


# ─── SAVE TOUR FLOW ───────────────────────────────────────────────────────────

def _ask_tour_name() -> str:
    """Ask the user for a tour name and return a non-empty string."""
    while True:
        name = input("Name this tour: ").strip()
        if name:
            return name
        print("Tour name cannot be empty. Please try again.")


def _ask_visibility() -> str:
    """Ask the user to choose between public and private visibility."""
    while True:
        print("\nVisibility:")
        print("  1. Public  (anyone with the token can view it, no login required)")
        print("  2. Private (the viewer must be logged in to see it)")
        choice = input("Choose 1 or 2: ").strip()
        if choice == "1":
            return "public"
        if choice == "2":
            return "private"
        print("Invalid choice. Please enter 1 or 2.")


def _ensure_places_saved(user_id: int, tour: Tour) -> bool:
    """
    Save any place in the tour that does not yet have a database id.
    Returns True if all places are persisted, False if any save fails.
    """
    for place in tour.places:
        if place.id is None:
            ok = save_place(user_id, place)
            if not ok:
                print(f"[Error] Could not save place '{place.name}' to the database.")
                return False
    return True


def save_tour_ui(user_id: int, tour: Tour):
    """
    Full interactive flow to name, set visibility, persist and display the
    share token for a tour.
    """
    tour.name = _ask_tour_name()
    tour.visibility = _ask_visibility()

    if not _ensure_places_saved(user_id, tour):
        print("Tour could not be saved because some places failed to persist.")
        return

    token = save_tour(user_id, tour)

    if token:
        display_share_token(token)
    else:
        print("[Error] Tour could not be saved to the database.")


# ─── LIST MY TOURS ────────────────────────────────────────────────────────────

def list_my_tours_ui(user_id: int):
    """
    Display all tours belonging to the current user, then offer to view one
    in detail or copy its share token.
    """
    tours = get_tours_by_user(user_id)

    if not tours:
        print("\nYou have no saved tours yet.")
        return

    print(f"\n══ Your Tours ({len(tours)}) ══")
    for i, meta in enumerate(tours, start=1):
        display_tour_summary(meta, index=i)

    print("\n  0. Back to main menu")
    choice = input(f"Select a tour to view (1-{len(tours)}) or 0 to go back: ").strip()

    if choice == "0" or not choice.isdigit():
        return

    idx = int(choice)
    if idx < 1 or idx > len(tours):
        print("Invalid selection.")
        return

    selected_meta = tours[idx - 1]
    tour_data = get_tour_by_token(selected_meta["share_token"])

    if tour_data:
        display_full_tour(tour_data)
        print(f"\n  Share token to send to others : {tour_data['share_token']}")


# ─── ACCESS A SHARED TOUR ─────────────────────────────────────────────────────

def access_shared_tour_ui(current_user_id: int | None):
    """
    Allow a user to access a tour via its share token.
    - Public tours are accessible without being logged in.
    - Private tours require the viewer to be logged in.
    """
    token = input("\nEnter the share token: ").strip()

    if not token:
        print("No token entered.")
        return

    tour_data = get_tour_by_token(token)

    if tour_data is None:
        print("[Error] No tour found with that token. Please check and try again.")
        return

    if tour_data["visibility"] == "private" and current_user_id is None:
        print("[Access denied] This tour is private. Please log in first to view it.")
        return

    display_full_tour(tour_data)