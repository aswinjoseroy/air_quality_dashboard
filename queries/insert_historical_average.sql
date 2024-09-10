INSERT INTO city_historical_averages (
    city, country, parameter_name, avg_3h, count_measurements, date_utc
) VALUES (
    %(city)s, %(country)s, %(parameter_name)s, %(avg_3h)s, %(count_measurements)s, %(date_utc)s
) ON CONFLICT (city, country, parameter_name, date_utc) DO NOTHING;
