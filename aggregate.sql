--- check date difference
SELECT
	*
FROM
	(
		SELECT
			tpep_pickup_datetime::date AS pickup_date,
			tpep_dropoff_datetime::date AS dropoff_date,
			total_amount,
			EXTRACT(DAY FROM tpep_pickup_datetime::timestamp - tpep_dropoff_datetime::timestamp) AS date_difference
		FROM
			trip_data
	)
WHERE
	date_difference > 0


--- AGGREGATE BY pickup date
SELECT
	pickup_date,
	SUM(total_amount) as total_amount
FROM
	(
		SELECT
			tpep_pickup_datetime::date AS pickup_date,
			total_amount
		FROM
			trip_data
	)
GROUP BY
	pickup_date
ORDER BY
	pickup_date ASC
