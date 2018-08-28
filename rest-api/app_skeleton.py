"""This is a part of an exercise from https://exercism.io/my/tracks/python"""
import json
import types
from table import Table

ACCESS_METHODS = ['GET', 'POST']
DEFAULT_INDEX = 'id'


class Application:
    """Allow to create rest applications."""
    def __init__(self):
        self.links = {m: {} for m in ACCESS_METHODS}
        self.database = None
        self.table_indexes = {}

    # Uggly hack, but I couldn't find a cleaner solution (PART 2):
    def __call__(self, tables):
        self.database = {}
        try:
            self.database = {table_name: (Table(table_name, table_content, self.get_table_index(table_name)))
                             for table_name, table_content in tables.items()}
        except KeyError as key:
            raise ValueError(f"No such database {key}")
        return self

    def add_tables_index(self, table_indexes):
        """Add indexes to the database, `table_indexes` argument is a dictionary
        mapping table names to their respective index column names.
        """
        for table_name, table_index in table_indexes.items():
            self.table_indexes[table_name] = table_index

    def get_table_index(self, table_name):
        """Return the index column name of the table named `table_name`."""
        try:
            return self.table_indexes[table_name]
        except KeyError:
            return DEFAULT_INDEX

    def route(self, url, method="GET"):
        """Add a route to our application, the default `method` is "GET", but "POST"
        is also accepted for this optional argument."""
        def decorate(function):
            if method not in ACCESS_METHODS:
                raise ValueError("We only provide the following access methods:", ACCESS_METHODS)
            self.links[method][url] = function
            return function
        return decorate

    def _request(self, method, url, payload):
        arguments = json.loads(payload) if payload else None
        result = self.links[method][url](self.database, arguments)
        if isinstance(result, types.GeneratorType):
            result = list(result)
        return json.dumps(result)

    def get(self, url, payload=None):
        """Route a "GET" request to the designated service."""
        return self._request("GET", url, payload)

    def post(self, url, payload=None):
        """Route a "POST" request to the designated service."""
        return self._request("POST", url, payload)
