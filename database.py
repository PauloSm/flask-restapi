import psycopg2
import sys
from config import DATABASE_PARAMS


class Database:
    """Class created to implement the methods used in the interaction with the database"""

    def __init__(self):
        self._connect()
        self.con = self._connect()
        self._create_table()

    def _connect(self) -> psycopg2:
        """
        Establishes connection with the database.
        Return: psycopg2 connection instance
        """
        try:
            '''
            con = psycopg2.connect(
                host="localhost",
                database="books",
                user="paulo",
                password="241089"
            )'''
            con = psycopg2.connect(**DATABASE_PARAMS) # unpack dictionary with database configurations
            return con
        except psycopg2.Error as error:
            self._error_handling(error.pgerror)

    def _create_table(self) -> None:
        """Creates a table if not found in the database."""
        try:
            cur = self.con.cursor()
            query = ("CREATE TABLE IF NOT EXISTS book (book_id serial NOT NULL PRIMARY KEY, "
                     "title varchar(200) NOT NULL UNIQUE, price varchar(10), description text, "
                     "url varchar(300) UNIQUE);")
            cur.execute(query)
        except psycopg2.Error as error:
            self._error_handling(error.pgerror)

    def insert_row(self, params: dict) -> None:
        """Insert data into the table"""
        cur = None
        try:
            cur = self.con.cursor()  # get cursor method responsible for execute queries
            sql = "INSERT INTO book(title, price, description, url) VALUES (%s, %s, %s, %s);"
            data = (params['title'], params['price'], params['description'], params['url'])
            try:
                cur.execute(sql, data)
            except psycopg2.IntegrityError:
                self.con.rollback()  # if the data has any type of integrity error the transaction is canceled
            else:
                self.con.commit()
        except psycopg2.Error as error:
            self._error_handling(error.pgerror)
        finally:
            if cur:
                cur.close()

    def close_connection(self) -> None:
        """Close the connection with the database"""
        self.con.close()

    def _error_handling(self, error_message: str) -> None:
        """Handle errors"""
        print(error_message)
        self.con.close()
        sys.exit(1)
