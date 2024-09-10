import json
import psycopg2
from datetime import datetime, timedelta
import os
from utils import load_sql_query
from process import process_message

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def load_sql_query(filename):
    """Load SQL query from a file."""
    with open(filename, 'r') as file:
        return file.read()


def lambda_handler(event, context):
    # logger.info(f"each event: {event}")
    # RDS parameters
    db_params = {
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'port': os.getenv('DB_PORT', 5432)
    }

    sql_queries = {
        'insert_location': load_sql_query('queries/insert_location.sql'),
        'insert_parameter': load_sql_query('queries/insert_parameter.sql'),
        'insert_measurement': load_sql_query('queries/insert_measurement.sql'),
        'calculate_recent_average': load_sql_query('queries/calculate_recent_average.sql'),
        'upsert_recent_average': load_sql_query('queries/upsert_recent_average.sql'),
        'upsert_city_geo_details': load_sql_query('queries/upsert_city_geo_details.sql'),
        'insert_historical_average': load_sql_query('queries/insert_historical_average.sql')
    }

    event_count = 0

    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                for record in event.get('Records'):
                    # print(f"each record: {record}")

                    # Parse the message body to extract the nested structure
                    record_body = json.loads(record['body'])
                    message_content = json.loads(record_body.get('Message'))

                    # Process the message content
                    process_message(cursor, message_content, sql_queries, logger)

                    event_count += 1

                # Commit the batch of transactions
                conn.commit()

        logger.info(f"Number of events processed: {event_count}")

    except Exception as e:
        print(f"An error occurred: {e}")
        raise e


