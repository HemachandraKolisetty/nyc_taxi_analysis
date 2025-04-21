SELECT 
    PULocationID, 
    DOLocationID, 
    round(avg(total_amount), 2) AS avg_fare,
    round(avg(date_diff('second', tpep_pickup_datetime, tpep_dropoff_datetime)) / 60, 2) AS avg_duration,
    count(*) AS trip_count
FROM yellow_taxi
GROUP BY PULocationID, DOLocationID
ORDER BY trip_count DESC
LIMIT 10;
