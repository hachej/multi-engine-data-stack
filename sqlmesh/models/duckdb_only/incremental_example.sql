MODEL (
    name reviews.incremental_example,
    kind INCREMENTAL_BY_TIME_RANGE (
        time_column event_date
    ),
    start '2020-01-01',
    cron '@daily',
    grain (id, event_date),
    allow_partials true
);

SELECT
    id,
    item_id,
    event_date
FROM
    reviews.raw_data_example
WHERE
    event_date BETWEEN @start_date AND @end_date;
