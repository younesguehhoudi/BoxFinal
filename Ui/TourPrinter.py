from Logic.Tour import Tour

def display_tour(tour: Tour):
    """Display the optimized tour in the console."""
    print("\n--- Optimized Tour ---")
    print(tour)
    print(f"Total distance: {tour.total_distance:.1f} km")