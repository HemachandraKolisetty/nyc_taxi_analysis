import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Read CSV; expected columns: route, pickup_hour, fare_std
df_vol = pd.read_csv("q3_fare_volatility.csv")
print("Columns:", df_vol.columns)  # Verify columns

# 2. Filter for routes with data for at least 12 distinct pickup hours
route_hours = df_vol.groupby("route")["pickup_hour"].nunique().reset_index(name="hour_count")
valid_routes = route_hours[route_hours["hour_count"] >= 12]["route"]

df_valid = df_vol[df_vol["route"].isin(valid_routes)]

# 3. Compute average volatility per route among valid routes
route_avg_vol = df_valid.groupby("route")["fare_std"].mean().reset_index()

# 4. Select top 5 routes with highest average fare volatility (among valid ones)
top_routes = route_avg_vol.nlargest(5, "fare_std")["route"].tolist()

# 5. Filter the dataset to include only these top routes
df_vol_top = df_valid[df_valid["route"].isin(top_routes)]

# 6. Create a line chart: x-axis = pickup_hour, y-axis = fare_std, one line per route
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_vol_top, x="pickup_hour", y="fare_std", hue="route", marker="o")
plt.title("Temporal Volatility in Fare by Route")
plt.xlabel("Hour of Day")
plt.ylabel("Fare Standard Deviation ($)")
plt.xticks(range(0, 24))
plt.legend(title="Route")
plt.tight_layout()
plt.show()
