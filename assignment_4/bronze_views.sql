-- create bronze_views table
DROP TABLE IF EXISTS miahenstridge.bronze_views;

CREATE EXTERNAL TABLE
miahenstridge.bronze_views (
    article STRING,
    views INT,
    rank INT,
    date DATE,
    retrieved_at STRING
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://mainong-wikidata-assignment4/datalake/views';
