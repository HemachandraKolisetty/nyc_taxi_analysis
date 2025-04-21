import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file (expected columns: PULocationID, fare_per_km)
df_aff = pd.read_csv("q5_route_affordability.csv")

# Group by pickup zone and compute the average fare per km
zone_aff = df_aff.groupby("PULocationID")["fare_per_km"].mean().reset_index()

# Select the top 10 pickup zones with the highest average fare per km
top10_zones = zone_aff.nlargest(10, "fare_per_km")

# Plot the bar chart
plt.figure(figsize=(10, 6))
sns.barplot(data=top10_zones, x="PULocationID", y="fare_per_km", palette="Blues_d")
plt.xlabel("Pickup Zone ID")
plt.ylabel("Average Fare per km ($/km)")
plt.title("Top 10 Pickup Zones with Highest Average Fare per km")
plt.tight_layout()
plt.show()
