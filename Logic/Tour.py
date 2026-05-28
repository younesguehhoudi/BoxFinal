from Logic.Place import Place

class Tour:
    def __init__(self, name, places, visibility):
        self.name = name
        self.places = places        
        self.visibility = visibility
        self.total_distance = 0.0
        self.share_token = None