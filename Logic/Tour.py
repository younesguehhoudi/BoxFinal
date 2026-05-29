class Tour:
    def __init__(self,name : str, places : list, visibility : str):
        self.name = name
        self.places = places
        self.visibility = visibility
        self.total_distance = 0.0
        self.share_token = ""

    def __str__(self):
        tour = " → ".join(str(i) for i in self.places)
        return f"Tour '{self.name}' : {tour} | {self.total_distance:.1f} km"