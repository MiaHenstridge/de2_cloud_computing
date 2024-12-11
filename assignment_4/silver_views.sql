-- create silver_views table
DROP TABLE IF EXISTS miahenstridge.silver_views;

CREATE TABLE miahenstridge.silver_views
    WITH (
        format='PARQUET',
        parquet_compression='SNAPPY',
        external_location='s3://mainong-wikidata-assignment4/datalake/silver_views'
    ) AS 
    SELECT
        article,
        views,
        rank,
        date
        -- cast(from_iso8601_timestamp(retrieved_at) AS TIMESTAMP) as retrieved_at
    FROM miahenstridge.bronze_views;