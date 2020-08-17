from library import *
from os import listdir, remove


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


    def print_db(self):
        print("\n\n[INFO]:: YOUR DATABASES:")
        for db in self.databases:
            print(f"\t[DB-{self.databases.index(db)}]:: {str(db).upper()}")

        print()

    def choose_db(self):

        self.print_db()

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
        return query

    def connect_db(self):
        self.databases[self.choose_db()]
        try:
            self.databases[query].db_connect()
            self.mdb = self.databases[query]
        except OperationalError:
            print("[FAIL]:: Can't access database: Wrong credentials")

    def delete_db(self):
        db = self.databases[self.choose_db()]
        remove(db.filename)
        self.databases.pop(self.databases.index(db))
        print(f"[INFO]:: Database '{db}' deleted")


    def active_database(self):
        for db in self.databases:
            if db.connected:
                return db

    def status(self):
        db = self.active_database()
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
        print("\t[OPTION 6]:: Delete database")
        print("\t[OPTION 0]:: exit")

        while True:
            try:
                self.option = int(input('[INPUT]:: '))
                print()
                break
            except ValueError:
                print("[FAIL]:: Invalid number! Try Again")
                print()

    def add_new_db(self):
        print("[QUERY]:: Type a unique name for your new database. Name is only for you and has nothing to do with the database itself.")
        name = input("[INPUT]:: ")
        if name:
            new_db = DataBase(name)
            self.databases.append(new_db)

            print("\n[INFO]:: Type credential for your database:")
            new_db.host = input("[QUERY]:: host: ")
            new_db.database = input("[QUERY]:: database: ")
            new_db.user = input("[QUERY]:: user: ")
            new_db.password = input("[QUERY]:: password: ")
            new_db.save_credentials()


    def run(self):

        my_program.setup()

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
                else:
                    print("[FAIL]:: You are not connected to any database")

            elif my_program.option == 4:
                if my_program.mdb:
                    my_program.mdb.close()
                else:
                    print("[WARNING]:: You are not connected to any database")

            elif my_program.option == 5:
                my_program.add_new_db()

            elif my_program.option == 6:
                my_program.delete_db()

            input("\n[INFO]: press Enter to continue...")
            print()
            my_program.menu()



if __name__ == "__main__":
    my_program = Program()
    my_program.run()


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
