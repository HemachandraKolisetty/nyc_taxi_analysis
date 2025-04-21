import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file (expected columns: PULocationID, DOLocationID, fare_per_km)
df_aff = pd.read_csv("q5_route_affordability.csv")

# Create a route column for clarity
df_aff["route"] = df_aff["PULocationID"].astype(str) + "->" + df_aff["DOLocationID"].astype(str)

# Group by route and compute the average fare per km (if multiple records exist)
route_aff = df_aff.groupby("route")["fare_per_km"].mean().reset_index()

# Select the top 10 most expensive routes by fare per km
top10_routes = route_aff.nlargest(10, "fare_per_km")

# Plot the horizontal bar chart
plt.figure(figsize=(10, 6))
sns.barplot(data=top10_routes, x="fare_per_km", y="route", palette="Reds_r")
plt.xlabel("Average Fare per km ($/km)")
plt.ylabel("Route (PU -> DO)")
plt.title("Top 10 Most Expensive Routes (Fare per km)")
plt.tight_layout()
plt.show()
