from users import User
import json
import utils
import sqlite3
from typing import Any
from users import Object


DEBUG = False


QUERIES = None
with open(utils.construct_path('queries.json'), "r") as file:
    QUERIES = json.load(file)


class Action:
    """
        Store the action on the object and build a querybased on this data
    """

    def __init__(self, name: str, obj: Object) -> None:
        self.name = name
        self.data = obj.get_data()

    def build_query(self) -> tuple:
        """Build a query based on the provided data"""
        if len(self.data['fields']) == 0:
            return None
        content = self.data.copy()
        content['fields'] = ', '.join(content['fields'])
        content['values'] = ', '.join([
            f"'{value}'" if type(value) == str else f"{value}"
            for value in content['values']
        ])
        query, request = QUERIES[self.name].values()
        query = query.format(**content)
        return query, self.name, request


class Database:
    """Create and manage the database"""

    def __init__(self, path: str = None) -> None:
        self.db_path = path if path else utils.construct_path('memory.sqlite')
        self.construct_db()

    def create_connection(self) -> sqlite3.Connection:
        """Create a connection with the database"""
        connection = None
        try:
            connection = sqlite3.connect(self.db_path)
            if DEBUG:
                print("Connection to SQLite DB successful")
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")
        return connection

    def execute_query(self,
                      query: str,
                      query_name: str = "noname",
                      request=True) -> Any:
        """Execute the query"""
        connection = self.create_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            if DEBUG:
                print(f"Query '{query_name}' executed successfully")
            if request:
                return cursor.fetchall()
            else:
                connection.commit()
        except sqlite3.Error as e:
            print(f"[execute_query]: The error '{e}' occurred\n\t{query}")

    def construct_db(self) -> None:
        """
            Create a database and the necessary tables
            if they don't already exist
        """
        path = utils.construct_path('construct_db_queries.json')
        with open(path, "r") as file:
            data = json.load(file)

        for query_name, query in data.items():
            self.execute_query(query, query_name, False)

    def perform(self, action: Action) -> Any:
        """Perform actions in the database"""
        return self.execute_query(
            *action.build_query()
        )

    def find_one(self, obj: Object):
        action = Action('find_one', obj)
        result = self.perform(action)
        if len(result) != 0:
            constr = type(obj)
            return constr(*result[0])
        return None

    def find(self, obj: Object):
        action = Action('find', obj)
        result = self.perform(action)
        if len(result) != 0:
            constr = type(obj)
            return [
                constr(*val)
                for val in result
            ]
        return None
