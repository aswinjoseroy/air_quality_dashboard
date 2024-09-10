INSERT INTO city_recent_averages (
    city, country, parameter_name, recent_avg_3h, count_measurements, date_utc
) VALUES (
    %(city)s, %(country)s, %(parameter_name)s, %(recent_avg_3h)s, %(count_measurements)s, %(date_utc)s
)
ON CONFLICT (city, country, parameter_name) DO UPDATE SET
    recent_avg_3h = EXCLUDED.recent_avg_3h,
    count_measurements = EXCLUDED.count_measurements,
    date_utc = EXCLUDED.date_utc;
