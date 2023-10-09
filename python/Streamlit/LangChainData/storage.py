import sqlite3
from sqlite3 import Error


class Storage:
    # constructor
    def __init__(self, db_file=".\db\test.db"):
        try:
            self.conn = self.create_connection(db_file)
            print(f"sqlite3.version = {sqlite3.version}")
            print(f"sqlite3.sqlite_version = {sqlite3.sqlite_version}")
        except Error as e:
            print(e)

        self.create_tables()

    def create_connection(self, db_file):
        """create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id integer PRIMARY KEY,
                name text NOT NULL,
                begin_date text,
                end_date text
            );
        """
        )

    def create_project(self, conn, project):
        """
        Create a new project into the projects table
        :param conn:
        :param project:
        :return: project id
        """
        sql = """ INSERT INTO projects(name,begin_date,end_date)
                VALUES(?,?,?) """
        cur = conn.cursor()
        cur.execute(sql, project)
        conn.commit()
        return cur.lastrowid
