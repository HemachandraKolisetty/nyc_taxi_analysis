# NYC Taxi Data Analysis: Machine Learning + Visualization

## Overview

This project analyzes NYC Yellow Taxi trip data to uncover spatial-temporal trends and forecast hourly fare and trip durations between any two NYC zones. Our goal is to empower commuters and city planners with an interactive system that delivers cost-effective, data-driven travel recommendations over a 24-hour window.

## Team

Akshay | Aditya | Chaturvedhi | Hema Chandra | Hima Varshini

---

## Objective

Despite the abundance of NYC taxi data, there's a lack of intelligent systems to forecast optimal travel times and pricing. We address this by:

- Predicting hourly fare and travel duration using machine learning.
- Visualizing hotspots and trends via interactive dashboards.
- Supporting informed decision-making for travelers and urban designers.

---

## Dataset

- **Source:** [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- **Data:** 2024 Yellow Taxi Trip Records (Jan–Dec)
- **Volume:** 41.17 million records (~661 MB Parquet format)
- **Features:** 19 (e.g., pickup/dropoff location, timestamps, fare, payment type)

---

## Methodology

### 🧠 ML Modeling

- **Model Used:** XGBoost Regressor
- **Target Variables:** Fare amount, Trip duration
- **Features:** 
  - Categorical: Pickup/Dropoff zones, payment type
  - Temporal: Hour of day, day of week (circular encoding)
  - Spatial: Geolocation clustering
- **Benchmark Models:** LSTM, SARIMAX (XGBoost outperformed both)

### 📊 Visualization

- Built with **React** + **D3.js**
- Interactive heatmaps and bubble plots
- Hourly prediction dashboard with affordability matrix

---

## Technical Stack

- **Backend/Data Processing:** Python, Pandas, AWS Athena, Spark
- **ML Frameworks:** scikit-learn, XGBoost
- **Visualization:** React, D3.js, Matplotlib, GeoJSON
- **Notebooks:** Jupyter for EDA and modeling

---

## Results

- **Model Performance:**
  - **Fare Prediction:** R² = 0.838 (train), 0.764 (test); RMSE = $3.35 / $4.10
  - **Duration Prediction:** R² = 0.743 (train), 0.721 (test); RMSE = 212 / 229 sec
- **Insights:**
  - Identified top 10 busiest zones by time of day
  - Visualized hourly demand fluctuations
  - Enabled simulations for dynamic pricing

---

## Conclusion

We developed a robust system combining ML and visualization to bridge the gap between raw NYC taxi data and actionable travel insights. The interactive dashboard allows users to compare hourly costs and durations, making this a powerful planning tool for commuters and city officials.

---

## Demo

> 🎥 Dashboard demo and screenshots will be added soon.

---

## License

This project is for educational purposes and follows the NYC TLC data usage guidelines.
