INSERT INTO air_quality_locations
(location_id, location_name, city, country, coordinates_lat, coordinates_long, is_mobile, is_analysis, entity, sensor_type)
VALUES (%(location_id)s, %(location_name)s, %(city)s, %(country)s, %(coordinates_lat)s, %(coordinates_long)s, %(is_mobile)s, %(is_analysis)s, %(entity)s, %(sensor_type)s)
ON CONFLICT (location_id) DO UPDATE
SET location_name = EXCLUDED.location_name, city = EXCLUDED.city, country = EXCLUDED.country,
    coordinates_lat = EXCLUDED.coordinates_lat, coordinates_long = EXCLUDED.coordinates_long,
    is_mobile = EXCLUDED.is_mobile, is_analysis = EXCLUDED.is_analysis, entity = EXCLUDED.entity,
    sensor_type = EXCLUDED.sensor_type;
