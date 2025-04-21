SELECT 
    hour(tpep_pickup_datetime) AS pickup_hour,
    round(avg(total_amount), 2) AS avg_fare
FROM yellow_taxi
GROUP BY hour(tpep_pickup_datetime)
ORDER BY pickup_hour;