from library import *
from os import listdir


class Program:
    def __init__(self):
        self.mdb = None
        self.databases = []
        self.option = None


    def setup(self):
        files  = listdir('.')
        print("[INFO]::Searching for saved databases...")
        for file in files:
            if file[-4:] == ".ini":
                name = file[1:-4]
                db = DataBase(name)
                db.get_credentials()
                self.databases.append(db)
                print(f"[INFO]::Added new Database: {name}")


    def choose_db(self):

        print("\n\n[INFO]:: YOUR DATABASES:")
        for db in self.databases:
            print(f"\t[DB-{self.databases.index(db)}]:: {str(db).upper()}")

        print()

        print(f"[QUERY]:: Choose database you want to be connected with (number from 0 to {self.databases.index(self.databases[-1])}):")
        while True:
            try:
                query = int(input("[INPUT]:: "))
                print()
                if query < 0 or query > self.databases.index(self.databases[-1]):
                    raise ValueError
                break
            except ValueError:
                print("[FAIL]:: Invalid number! Try Again")

        try:
            self.databases[query].db_connect()
            self.mdb = self.databases[query]
        except psycopg2.OperationalError:
            print("[FAIL]:: Can't access database: Wrong user or password")


    def active_database(self):
        for db in self.databases:
            if db.connected:
                return db

    def status(self):
        db = my_program.active_database()
        if db:
            return f"[INFO]:: You are connected to {db}"
        else:
            return "[INFO]:: You are not connected to any database"


    def menu(self):
        print("\n[MENU]::")
        print("\t[OPTION 1]:: Check connection status")
        print("\t[OPTION 2]:: Choose database to connect with")
        print("\t[OPTION 3]:: View tables of the active database")
        print("\t[OPTION 4]:: Close conection with current database")
        print("\t[OPTION 5]:: Add new database")
        print("\t[OPTION 0]:: exit")

        while True:
            try:
                self.option = int(input('[INPUT]:: '))
                print()
                break
            except ValueError:
                print("[FAIL]:: Invalid number! Try Again")
                print()

    def main(self):
        while True:
            if my_program.option == 0:
                break
            elif my_program.option == 1:
                print(my_program.status())
            elif my_program.option == 2:
                my_program.choose_db()
            elif my_program.option == 3:
                if my_program.mdb:
                    my_program.mdb.get_table_names()
                    my_program.mdb.tables_view()
            input("\n[INFO]: press Enter to continue...")
            print()
            my_program.menu()



if __name__ == "__main__":

    my_program = Program()

    my_program.setup()
    my_program.main()


    ### Temp 1
    # ep = databases[0]
    # ep.db_connect()
    # ep.get_table_names()
    # for tab in ep.tables:
    #     ep.get_column_names(tab)


    ### Temporary
    # mdb = databases[1]
    # mdb.db_connect()
    # mdb.get_table_names()
    # for tab in mdb.tables:
    #     mdb.get_column_names(tab)
