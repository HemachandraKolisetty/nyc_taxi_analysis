SELECT 
  concat(cast(PULocationID as varchar), '->', cast(DOLocationID as varchar)) AS route,
  round(stddev(total_amount), 2) AS fare_std,
  count(*) AS trip_count
FROM yellow_taxi
GROUP BY 
  concat(cast(PULocationID as varchar), '->', cast(DOLocationID as varchar))
ORDER BY fare_std DESC;