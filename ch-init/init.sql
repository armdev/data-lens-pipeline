-- The Final Analytical Table
CREATE TABLE IF NOT EXISTS events (
    id Int32,
    event_type String,
    value Float64,
    created_at DateTime64(3, 'UTC')
) ENGINE = ReplacingMergeTree() 
ORDER BY (id, created_at);

-- The Kafka Queue (Ingestion Engine)
CREATE TABLE IF NOT EXISTS events_queue (
    id Int32,
    event_type String,
    value Float64,
    created_at Int64 -- Debezium sends timestamps as epochs
) ENGINE = Kafka 
SETTINGS kafka_broker_list = 'redpanda:9092',
         kafka_topic_list = 'cdc.public.events',
         kafka_group_name = 'clickhouse_consumers',
         kafka_format = 'JSONEachRow';

-- The Glue (Materialized View)
CREATE MATERIALIZED VIEW IF NOT EXISTS events_mv TO events AS
SELECT 
    id, 
    event_type, 
    value, 
    toDateTime64(created_at / 1000, 3) AS created_at
FROM events_queue;
