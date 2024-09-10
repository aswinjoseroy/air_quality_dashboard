INSERT INTO air_quality_measurements (
    location_id, parameter_name, value, date_utc, date_local
) VALUES (
    %(location_id)s, %(parameter_name)s, %(value)s, %(date_utc)s, %(date_local)s
) ON CONFLICT (location_id, parameter_name, date_utc) DO NOTHING;
