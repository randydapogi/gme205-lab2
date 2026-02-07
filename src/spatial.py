import math
import csv

class Point: 
    def __init__(self, id, lon, lat, name=None, tag=None):
        if not (-180 <= lon <= 180): 
            raise ValueError("Longitude must be between -180 and 180") 
        if not (-90 <= lat <= 90): 
            raise ValueError("Latitude must be between -90 and 90") 
        
        self.id = id 
        self.lon = lon 
        self.lat = lat
        self.name = name 
        self.tag = tag
        
    # ------------------------------------------------------------------
    # Instance methods (behavior belongs to the object) 
    # ------------------------------------------------------------------ 
    def to_tuple(self) -> tuple[float, float]: 
        """ Return the coordinate as a (lon, lat) tuple. """ 
        return (self.lon, self.lat)
    
    def distance_to(self, other): 
        return Point.haversine_m(self.lon, self.lat, other.lon, other.lat)
    
    def is_poi(self): 
        return (self.tag or "").lower() == "poi"
    
    # ------------------------------------------------------------------ 
    # Static method (pure spatial math) 
    # ------------------------------------------------------------------ 
    @staticmethod 
    def haversine_m( lon1: float, lat1: float, lon2: float, lat2: float ) -> float: 
        """ Compute the Haversine distance between two lon/lat pairs in meters. Static method because it does not depend on object state. """ 
        R = 6_371_000.0 # Earth radius in meters 
        
        phi1 = math.radians(lat1) 
        phi2 = math.radians(lat2) 
        dphi = math.radians(lat2 - lat1) 
        dlambda = math.radians(lon2 - lon1)
         
        a = ( math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2 ) 
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)) 
        
        return R * c
    
    # ------------------------------------------------------------------ 
    # Class method (constructing objects from data) 
    # ------------------------------------------------------------------ 
    @classmethod 
    def from_row(cls, row): 
        return cls( 
                   id=str(row["id"]), 
                   lon=float(row["lon"]), 
                   lat=float(row["lat"]), 
                   name=row.get("name"), 
                   tag=row.get("tag"), 
                )
        
        
class PointSet:
    def __init__(self, points: list[Point]):
        self.points = points
        
    @classmethod
    def from_csv(cls, csv_path: str):
        # open csv
        # read csv syntax from gemini
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        points = []
        for row in rows:
            # only add points with valid coordinate to points list
            try:
                point = Point.from_row(row)
                points.append(point)
            except ValueError:
                print(f"Row with id {row["id"]} has invalid coordinates.")
                
        return cls(points=points)