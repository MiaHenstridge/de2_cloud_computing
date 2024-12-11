-- create silver_views table
DROP TABLE IF EXISTS mainong.silver_views;

CREATE TABLE mainong.silver_views
    WITH (
        format='PARQUET',
        parquet_compression='SNAPPY',
        external_location='s3://mainong-wikidata-assignment4/datalake/silver_views'
    ) AS 
    SELECT
        article,
        views,
        rank,
        date,
    FROM mainong.bronze_views;