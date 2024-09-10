INSERT INTO city_geo_details (city, country, latitude, longitude)
VALUES (%(city)s, %(country)s, %(latitude)s, %(longitude)s)
ON CONFLICT (city, country)
DO UPDATE SET
    latitude = EXCLUDED.latitude,
    longitude = EXCLUDED.longitude;
