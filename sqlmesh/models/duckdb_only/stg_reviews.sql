MODEL (
    name reviews.stg_reviews,
    kind FULL,
    columns (
        reviewid string,
        username string,
        review string,
        ingestion_date timestamp
    ),
    enabled @IF(@gateway='duckdb', True, False)
);

SELECT 
    reviewid,
    username,
    review,
    epoch_ms(ingestion_date) as ingestion_date              
FROM landing_reviews
QUALIFY
    row_number() OVER (PARTITION BY username, review ORDER BY ingestion_date) = 1;


