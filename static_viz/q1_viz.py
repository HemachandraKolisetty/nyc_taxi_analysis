import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Read CSV; expected columns: route, pickup_hour, avg_fare
df_fare = pd.read_csv("q1_hourly_fare_route.csv")
print("Columns:", df_fare.columns)  # For verification

# 2. Determine the most popular routes based on frequency in the CSV file
route_counts = df_fare.groupby("route").size().reset_index(name="count")
top_routes = route_counts.nlargest(20, "count")["route"].tolist()

# 3. Filter the dataframe to include only the top routes
df_fare_top = df_fare[df_fare["route"].isin(top_routes)]

# 4. Pivot for Heatmap: index = route, columns = pickup_hour, values = avg_fare
heatmap_data = df_fare_top.pivot(index="route", columns="pickup_hour", values="avg_fare")

# 5. Plot Heatmap
plt.figure(figsize=(14, 8))
sns.set(style="whitegrid")
sns.heatmap(
    heatmap_data,
    annot=True, fmt=".2f",  # Show numeric values in each cell
    cmap="viridis",
    cbar_kws={"label": "Avg Fare ($)"}
)
plt.title("Hourly Fare Heatmap by Route (Top 20 Popular Routes)")
plt.xlabel("Pickup Hour (0-23)")
plt.ylabel("Route (PU->DO)")
plt.tight_layout()
plt.show()
