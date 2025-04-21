SELECT 
    hour(tpep_pickup_datetime) AS pickup_hour,
    round(avg(date_diff('second', tpep_pickup_datetime, tpep_dropoff_datetime)) / 60, 2) AS avg_duration
FROM yellow_taxi
GROUP BY hour(tpep_pickup_datetime)
ORDER BY pickup_hour;