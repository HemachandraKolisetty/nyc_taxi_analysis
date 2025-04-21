import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Read CSV file (ensure it has the expected columns)
df_stability = pd.read_csv("q4_route_stability.csv")
print("Columns:", df_stability.columns)

# (Optional) Filter to include only routes with a minimum number of trips (if 'trip_count' column exists)
if "trip_count" in df_stability.columns:
    df_stability = df_stability[df_stability["trip_count"] >= 50]  # adjust threshold as needed

# 2. Sort the routes by fare volatility (standard deviation)
df_stability = df_stability.sort_values("fare_std", ascending=False)

# (Optional) Limit to top 20 routes for visualization clarity
df_top = df_stability.head(20)

# 3. Plot a horizontal bar chart
plt.figure(figsize=(10, 8))
sns.barplot(data=df_top, x="fare_std", y="route", palette="Spectral")
plt.title("Most Volatile vs. Most Stable Routes (Fare Standard Deviation)")
plt.xlabel("Fare Standard Deviation ($)")
plt.ylabel("Route (PU -> DO)")
plt.tight_layout()
plt.show()
