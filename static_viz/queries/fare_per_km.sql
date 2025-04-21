SELECT 
  PULocationID,
  DOLocationID,
  round(avg(total_amount / nullif(trip_distance, 0)), 2) AS fare_per_km
FROM yellow_taxi
WHERE trip_distance > 0
GROUP BY PULocationID, DOLocationID
ORDER BY fare_per_km DESC;