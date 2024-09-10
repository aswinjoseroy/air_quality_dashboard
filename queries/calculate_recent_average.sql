SELECT AVG(am.value) AS recent_avg_3h, COUNT(*) AS measurement_count
FROM air_quality_measurements am
WHERE am.location_id IN (
    SELECT location_id
    FROM air_quality_locations
    WHERE city = %(city)s
      AND country = %(country)s
)
AND am.parameter_name = %(parameter_name)s
AND am.date_utc >= %(time_window)s;
