import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Read CSV file (adjust filename if needed)
df = pd.read_csv("q6_time_cost_tradeoff.csv")
print("Columns:", df.columns)

# 2. Calculate the number of records per route
route_counts = df.groupby('route').size().reset_index(name='count')

# 3. For each route, calculate the correlation between avg_fare and avg_duration
def calc_corr(group):
    # Only calculate if there are at least 2 data points
    if len(group) < 2:
        return None
    return group['avg_fare'].corr(group['avg_duration'])

corr_by_route = df.groupby('route').apply(calc_corr).reset_index(name='corr')

# 4. Merge with route_counts so we can filter by sample size
corr_by_route = corr_by_route.merge(route_counts, on='route')

# 5. Filter routes with at least a minimum number of data points (e.g., 10)
filtered_routes = corr_by_route[corr_by_route['count'] >= 10].copy()

# 6. Compute absolute correlation and select top 3 routes with the strongest relationship
filtered_routes['abs_corr'] = filtered_routes['corr'].abs()
top_routes = filtered_routes.nlargest(3, 'abs_corr')['route'].tolist()
print("Selected routes for visualization:", top_routes)

# 7. Filter the main dataframe for these selected routes
df_top = df[df['route'].isin(top_routes)].copy()

# 8. Plot scatter plots with regression lines using Seaborn's lmplot
sns.set(style="whitegrid")

lm = sns.lmplot(
    data=df_top,
    x="avg_duration", 
    y="avg_fare", 
    col="route",         # Create one facet per route
    hue="route",         # Color by route
    aspect=0.8,
    markers="o",
    ci=None,             # No confidence interval shading
    scatter_kws={'s': 50}
)
lm.set_axis_labels("Average Trip Duration (min)", "Average Fare ($)")
lm.fig.suptitle("Time-to-Cost Tradeoff: Avg Fare vs. Avg Duration for Selected Routes", y=1.03)
plt.show()
