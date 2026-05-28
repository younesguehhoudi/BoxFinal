class Place:
    def __init__(self,name,lat,lng):
        self.name = name
        self.lat = lat
        self.lng = lng 
        
    def __str__(self):
        return f"{self.name} ({self.lat}, {self.lng})"
    