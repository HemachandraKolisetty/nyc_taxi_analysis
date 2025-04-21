import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set a common style for the plots
sns.set(style="whitegrid")

##############################
# 1. Hourly Fare Forecast
##############################
# CSV file: hourly_fare.csv (columns: pickup_hour, avg_fare)
df_fare = pd.read_csv("hourly_fare_forecast.csv")
plt.figure(figsize=(10, 6))
sns.barplot(data=df_fare, x="pickup_hour", y="avg_fare", palette="viridis")
plt.xlabel("Hour of Day")
plt.ylabel("Average Fare ($)")
plt.title("Hourly Fare Forecast")
plt.xticks(range(0, 24))
plt.tight_layout()
plt.show()

##############################
# 2. Hourly Trip Duration Forecast
##############################
# CSV file: hourly_duration.csv (columns: pickup_hour, avg_duration)
df_duration = pd.read_csv("hourly_trip_duration.csv")
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_duration, x="pickup_hour", y="avg_duration", marker="o", color="orange")
plt.xlabel("Hour of Day")
plt.ylabel("Average Trip Duration (minutes)")
plt.title("Hourly Trip Duration Forecast")
plt.xticks(range(0, 24))
plt.tight_layout()
plt.show()

##############################
# 3. Top OD Route Summary (Forecast Cards)
##############################
# CSV file: top_od_route.csv (columns: PULocationID, DOLocationID, avg_fare, avg_duration, trip_count)
df_od = pd.read_csv("trip_pu_do_summary.csv")
# Create a new column to label the route (e.g., "132 -> 236")
df_od["OD_Route"] = df_od["PULocationID"].astype(str) + " -> " + df_od["DOLocationID"].astype(str)

plt.figure(figsize=(12, 8))
# Scatter plot: x-axis average duration, y-axis average fare, bubble size = trip count
sns.scatterplot(data=df_od, x="avg_duration", y="avg_fare", size="trip_count", sizes=(100, 1000), hue="OD_Route", legend=False)
plt.xlabel("Average Trip Duration (minutes)")
plt.ylabel("Average Fare ($)")
plt.title("Top OD Route Summary: Fare vs. Duration (Bubble size = Trip Count)")

# Annotate each point with its OD route label
for index, row in df_od.iterrows():
    plt.text(row["avg_duration"], row["avg_fare"], row["OD_Route"], fontsize=9, alpha=0.8)

plt.tight_layout()
plt.show()

##############################
# 4. Pickup Demand by Location
##############################
# CSV file: pickup_demand.csv (columns: PULocationID, pickup_count)
df_pickup = pd.read_csv("pickup_demand_heatmap_data.csv")

# Sort by pickup_count descending, then take top 20
df_top = df_pickup.nlargest(20, "pickup_count")

plt.figure(figsize=(12, 6))
sns.barplot(data=df_top, x="PULocationID", y="pickup_count", palette="magma")
plt.xlabel("Pickup Location ID")
plt.ylabel("Number of Pickups")
plt.title("Pickup Demand by Location (Top 20)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
