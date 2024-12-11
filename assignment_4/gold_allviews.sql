-- create gold_allviews table
DROP TABLE IF EXISTS miahenstridge.gold_allviews;

CREATE TABLE miahenstridge.gold_allviews
    WITH (
        format='PARQUET',
        parquet_compression='SNAPPY',
        external_location='s3://mainong-wikidata-assignment4/datalake/gold_allviews'
    ) AS 
    SELECT
        article,
        SUM(views) AS total_top_view,
        MIN(rank) AS top_rank,
        COUNT(date) AS ranked_days
    FROM miahenstridge.silver_views
    GROUP BY article;

