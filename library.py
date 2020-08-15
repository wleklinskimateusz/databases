from psycopg2 import connect, sql

class Column:
    def __init__(self, name):
        self.name = name
        print(f"[INFO]:: adding new column {self.name}")

    def __repr__(self):
        return self.name


class Table:
    def __init__(self, name):
        self.name = name
        self.columns = []
        print(f"[INFO]:: adding new table: {self.name}")

    def __repr__(self):
        return self.name

class DataBase:
    def __init__(self,name,host=None, database=None, user=None, password=None):
        self.name = name
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

        self.filename = f".{self.name}.ini"

        self.connected = False

        self.tables = []

    def __repr__(self):
        """
        how object is represented when called
        """
        if self.name:
            return self.name
        else:
            return "empty database"

    def db_connect(self):
        """
        starts connection with database
        """

        print(f"Conecting to database {self.name}...")

        self.connection = connect(
            host = self.host,
            database = self.database,
            user = self.user,
            password = self.password
        )
        self.cursor = self.connection.cursor()
        self.connected = True

        print("Success!")

    def close(self, save_changes=True):
        """
        closes connection with database
        """
        if save_changes:
            self.connection.commit()

        self.cursor.close()
        self.connection.close()
        self.cursor = None
        self.connection = None
        self.connected = False

    def save_credentials(self):
        """
        saves credentials to the file
        """
        if self.host and self.database and self.user and self.password:
            with open(self.filename, "w") as credentials:
                credentials.write(self.host + "\n")
                credentials.write(self.database + "\n")
                credentials.write(self.user + "\n")
                credentials.write(self.password)
        else:
            print("[FAIL] :: Some credentials are missing")

    def get_credentials(self, file=None):
        """
        reads credential from the file
        """
        if not file:
            file = self.filename
        with open(file, "r") as credentials:
            [
                self.host,
                self.database,
                self.user,
                self.password
            ] = credentials.readlines()

            # Gets rid of "\n"
            self.host = self.host.replace("\n", "")
            self.database = self.database.replace("\n", "")
            self.user = self.user.replace("\n", "")
            self.password = self.password.replace("\n", "")

    def credentials(self):
        """
        gives a list of all credentials
        """
        return [
            self.host,
            self.database,
            self.user,
            self.password
        ]

    def sql_select(self, table, columns="*", where=None):
        """
        a method to write select statements in sql
        """

        if self.connected:
            self.cursor.execute(f"SELECT * FROM {table}")
            return self.cursor.fetchone()
        else:
            print("[FAIL]:: You are not connected to database!")

    def sql_insert(self, table, values, columns=None):
        """
        a method to insert values to tables
        """
        if self.connected:
            command = f"INSERT INTO {table} "
            if columns:
                command += "("
                for column in columns:
                    command += f"{column}, "
                command = command[:-2] # gets rid of last colon and space
                command += ") "
            command += "VALUES ("
            for value in values:
                command += f"{value}, "
            command = command[:-2]
            command += ");"
        else:
            print("[FAIL]:: You are not connected to database.")


    def sql(self, command):
        """
        a method to execute  other sql commands
        """
        if self.connected:
            self.cursor.execute(command)
        else:
            print("[FAIL]:: You are not connected to database.")


    def get_table_names(self):
        """
        a method that returns list of table names
        """
        tables = []
        if self.connected:
            self.cursor.execute("""
            SELECT table_name
            FROM INFORMATION_SCHEMA.tables
            WHERE table_schema = 'public'""")
            for table in self.cursor.fetchall():
                tables.append(Table(table[0]))

            self.tables = tables
        else:
            print("[FAIL]:: You are not connected to database.")


    def get_column_names(self, table):
        """
        a method that returns a list of column names in a table
        """
        if self.connected:

            col_names_str = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE "
            col_names_str += f"table_name = '{table}';"

            try:
                sql_object = sql.SQL(
                    col_names_str
                ).format(
                    sql.Identifier(str(table))
                )

                self.cursor.execute(sql_object)

                col_names = (self.cursor.fetchall() )

                print(f"\n[INFO]:: Column names in {table}: " + str(col_names))

                for col_name in col_names:
                    table.columns.append(Column(col_name[0]))

            except Exception as err:
                print("get_columns_names ERROR: ", err)

        else:
            print("[FAIL]:: You are not connected to database.")
