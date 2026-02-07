from spatial import Point, PointSet

# B.2.3
# p = Point("A", 121.0, 14.6) 
# print(p.id, p.lon, p.lat) 

# B.3.3
# q = Point("X", 999, 14) 
# print(q.id, q.lon, q.lat)

# B.5.4
# p = Point("A", 121.0, 14.6) 
# print(p.id, p.lon, p.lat) 
# print(p.to_tuple())

# # Distance to Test
# p1 = Point("A", 121.0, 14.6) 
# p2 = Point("A", 121.4, 14.23)

# print(f"Point {p1.id} ({p1.lat}, {p1.lat}) is {p1.distance_to(p2)} meters to {p2.id} ({p2.lat}, {p2.lat}).")



# create pointset from csv
csv_path = "data/points.csv"
pointset = PointSet.from_csv(csv_path)
print(pointset.count())
print(pointset.bbox())

# create filtered pointset from pointset
filtered_pointset = pointset.filter_by_tag("poi")
print(filtered_pointset.count())
print(filtered_pointset.bbox())


pointset.plot_lat_lon("output/lab2_preview.png")
pointset.generate_summary_json("output/lab2_report.json")
# filtered_pointset.plot_lat_lon("output/lab2_preview_poi.png")
