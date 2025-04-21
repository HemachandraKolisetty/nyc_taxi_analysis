SELECT 
    PULocationID, 
    count(*) AS pickup_count
FROM yellow_taxi
GROUP BY PULocationID
ORDER BY pickup_count DESC;
