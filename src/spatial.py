import math
import pandas as pd
import matplotlib.pyplot as plt
import json

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
        try: 
            df = pd.read_csv(csv_path)
        except FileNotFoundError:
            raise 
        
        points = []
        for index, row in df.iterrows():
            # only add points with valid coordinate to points list
            try:
                point = Point.from_row(row)
                points.append(point)
            except ValueError:
                print(f"Row with id {row["id"]} has invalid coordinates.")
                
        return cls(points=points)
    
    # return length of points
    def count(self):
        return len(self.points)
    
    # return bbox of points
    def bbox(self):
        if len(self.points) == 0:
            return None
        
        lat_list = self.get_lat_list()
        lon_list = self.get_lon_list()
        
        min_lat = min(lat_list)
        max_lat = max(lat_list)
        
        min_lon = min(lon_list)
        max_lon = max(lon_list)
        
        return (min_lon, min_lat, max_lon, max_lat)
    
    # returns pointset with tag
    def filter_by_tag(self, tag: str):
        # filter points with same tag
        filtered_points = [p for p in self.points if p.tag == tag]
        
        return PointSet(points=filtered_points)
    
    def get_lat_list(self):
        return [p.lat for p in self.points]
    
    def get_lon_list(self):
        return [p.lon for p in self.points]
    
    def plot_lat_lon(self, output_path):
        # Save scatter plot (valid coords only)
        plt.figure() 
        if len(self.points) == 0: 
            # Create an empty plot with message in title
            plt.title("Preview Plot (No valid coordinates to plot)")
        else: 
            lat_list = self.get_lat_list()
            lon_list = self.get_lon_list()
            
            plt.scatter(lon_list, lat_list)
            plt.title("Point Preview (lon vs lat)")
            plt.xlabel("Longitude")
            plt.ylabel("Latitude")
            plt.savefig(output_path, dpi=150, bbox_inches="tight")
            plt.close()
            
    def generate_summary_json(self, output_path):
        summary = {
            "total_points": self.count(),
            "bbox": self.bbox()
        }
        
        counts = {}
        for point in self.points:
            tag = point.tag
            counts[tag] = counts.get(tag, 0) + 1
            
        summary["tags"] = [{k: v} for k, v in counts.items()]
        
        with open(output_path, "w", encoding="utf-8") as f: 
            json.dump(summary, f, indent=2)
        