from spatial import PointSet
import matplotlib.pyplot as plt
import json

# get pointset from csv
csv_path = "data/points.csv"
pointset = PointSet.from_csv(csv_path)

print(pointset.count())
print(pointset.bbox())

# create filtered pointset from pointset
filtered_pointset = pointset.filter_by_tag("poi")
print(filtered_pointset.count())
print(filtered_pointset.bbox())

# Generate lat lon plot preview
output_plot_path = "output/lab2_preview.png"
plt.figure() 
if len(pointset.points) == 0: 
    # Create an empty plot with message in title
    plt.title("Preview Plot (No valid coordinates to plot)")
else: 
    lat_list = pointset.get_lat_list()
    lon_list = pointset.get_lon_list()
    
    plt.scatter(lon_list, lat_list)
    plt.title("Point Preview (lon vs lat)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.savefig(output_plot_path, dpi=150, bbox_inches="tight")
    plt.close()
    
# Generate summary json
output_summary_path = "output/lab2_report.json"
summary = {
    "total_points": pointset.count(),
    "bbox": pointset.bbox()
}

counts = {}
for point in pointset.points:
    tag = point.tag
    counts[tag] = counts.get(tag, 0) + 1
    
summary["tags"] = [{k: v} for k, v in counts.items()]

with open(output_summary_path, "w", encoding="utf-8") as f: 
    json.dump(summary, f, indent=2)