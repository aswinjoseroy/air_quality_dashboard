def load_sql_query(filename):
    """Load SQL query from a file."""
    with open(filename, 'r') as file:
        return file.read()
