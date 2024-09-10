from datetime import datetime, timedelta, timezone


def process_message(cursor, message_body, sql_queries, logger):
    """Process a single SQS message and update the RDS tables accordingly"""

    data = {
        "location_id": message_body['locationId'],
        "location_name": message_body['location'],
        "city": message_body['city'],
        "country": message_body['country'],
        "coordinates_lat": message_body['coordinates']['latitude'],
        "coordinates_long": message_body['coordinates']['longitude'],
        "is_mobile": message_body['isMobile'],
        "is_analysis": message_body['isAnalysis'],
        "entity": message_body['entity'],
        "sensor_type": message_body['sensorType'],
        "parameter_name": message_body['parameter'],
        "value": message_body['value'],
        "unit": message_body['unit'],
        "date_utc": message_body['date']['utc'],
        "date_local": message_body['date']['local']
    }

    # Insert or update location information
    cursor.execute(sql_queries['insert_location'], data)

    # Insert or update parameter information
    cursor.execute(sql_queries['insert_parameter'], data)

    # Insert measurement data
    cursor.execute(sql_queries['insert_measurement'], data)

    # Upsert city geo details
    cursor.execute(sql_queries['upsert_city_geo_details'], {
        'city': data['city'],
        'country': data['country'],
        'latitude': data['coordinates_lat'],
        'longitude': data['coordinates_long']
    })

    desired_offset = timezone(timedelta(hours=2))

    date_utc_str = data['date_utc']
    date_utc = datetime.fromisoformat(date_utc_str)

    if date_utc.tzinfo is None:
        date_utc = date_utc.replace(tzinfo=timezone.utc)

    # Calculate the time window by subtracting 3 hours from 'date_utc'
    time_window = date_utc - timedelta(hours=3)

    time_window_iso = time_window.isoformat()

    if data["city"] and data["country"]:

        cursor.execute(sql_queries['calculate_recent_average'], {
            "city": data["city"],
            "country": data["country"],
            "parameter_name": data["parameter_name"],
            "time_window": time_window_iso,
            "date_utc": data['date_utc']
        })

        avg_result = cursor.fetchone()

        if avg_result:
            avg_value, measurement_count = avg_result

            # Insert or update the recent average in city_recent_averages table
            cursor.execute(sql_queries['upsert_recent_average'], {
                "city": data["city"],
                "country": data["country"],
                "parameter_name": data["parameter_name"],
                "recent_avg_3h": avg_value,
                "count_measurements": measurement_count,
                "date_utc": data['date_utc']
            })

            # Insert the historical average into city_historical_averages table
            cursor.execute(sql_queries['insert_historical_average'], {
                "city": data["city"],
                "country": data["country"],
                "parameter_name": data["parameter_name"],
                "avg_3h": avg_value,
                "count_measurements": measurement_count,
                "date_utc": data['date_utc']
            })
