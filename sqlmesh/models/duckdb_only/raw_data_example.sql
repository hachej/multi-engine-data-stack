MODEL (
    name reviews.raw_data_example,
    kind VIEW
);

SELECT
    CAST(id AS INTEGER),
    CAST(item_id AS VARCHAR),
    CAST(event_date AS DATE)
FROM (
    VALUES
        (1, 'item_1', '2020-01-01'),
        (2, 'item_2', '2020-01-02'),
        (3, 'item_3', '2020-01-03'),
        (4, 'item_4', '2020-01-04'),
        (5, 'item_5', '2020-01-05'),
        (6, 'item_6', '2020-01-06'),
        (7, 'item_7', '2020-01-07'),
        (8, 'item_8', '2020-01-08'),
        (9, 'item_9', '2020-01-09'),
        (10, 'item_10', '2020-01-10')
) AS t(id, item_id, event_date);

