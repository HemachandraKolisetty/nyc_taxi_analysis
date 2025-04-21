CREATE EXTERNAL TABLE nyc_taxi_data.yellow_taxi (
    vendorid int,
    tpep_pickup_datetime timestamp,
    tpep_dropoff_datetime timestamp,
    passenger_count bigint,
    trip_distance double,
    ratecodeid bigint,
    store_and_fwd_flag string,
    pulocationid int,
    dolocationid int,
    payment_type int,
    fare_amount double,
    extra double,
    mta_tax double,
    tip_amount double,
    tolls_amount double,
    improvement_surcharge double,
    total_amount double,
    congestion_surcharge double,
    airport_fee double
)
STORED AS PARQUET
LOCATION 's3://cse6242-ashukla301/'
TBLPROPERTIES ('has_encrypted_data'='false');
