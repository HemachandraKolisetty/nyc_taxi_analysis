SELECT 
  concat(cast(PULocationID as varchar), '->', cast(DOLocationID as varchar)) AS route,
  hour(tpep_pickup_datetime) AS pickup_hour,
  round(avg(total_amount), 2) AS avg_fare
FROM yellow_taxi
GROUP BY 
  concat(cast(PULocationID as varchar), '->', cast(DOLocationID as varchar)), 
  hour(tpep_pickup_datetime)
ORDER BY route, pickup_hour;
