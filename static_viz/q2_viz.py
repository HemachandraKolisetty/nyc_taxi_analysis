import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Read CSV; expected columns: route, pickup_hour, avg_duration
df_dur = pd.read_csv("q2_hourly_duration_route.csv")
print("Columns:", df_dur.columns)  # Verify the column names

# 2. Determine the most popular routes based on record frequency
route_counts = df_dur.groupby("route").size().reset_index(name="count")
top_routes = route_counts.nlargest(20, "count")["route"].tolist()

# 3. Filter the dataframe to include only the top routes
df_dur_top = df_dur[df_dur["route"].isin(top_routes)]

# 4. Pivot the data: index = route, columns = pickup_hour, values = avg_duration
heatmap_data = df_dur_top.pivot(index="route", columns="pickup_hour", values="avg_duration")

# 5. Plot the Heatmap
plt.figure(figsize=(14, 8))
sns.set(style="whitegrid")
sns.heatmap(
    heatmap_data,
    annot=True, fmt=".2f",    # Annotate each cell with numeric values (2 decimal places)
    cmap="magma",            # Choose a colormap (magma, viridis, etc.)
    cbar_kws={"label": "Avg Duration (min)"}
)
plt.title("Hourly Duration Heatmap by Route (Top 20 Popular Routes)")
plt.xlabel("Pickup Hour (0–23)")
plt.ylabel("Route (PU->DO)")
plt.tight_layout()
plt.show()
