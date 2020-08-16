from library import *
from os import listdir


def write_db():
    files  = listdir('.')
    databases = []
    print("[INFO]::Searching for saved databases...")
    for file in files:
        if file[-4:] == ".ini":
            name = file[1:-4]
            db = DataBase(name)
            db.get_credentials()
            databases.append(db)
            print(f"[INFO]::Added new Database: {name}")
    return databases

def setup():
    databases = write_db()

    print("\n\n[INFO]:: YOUR DATABASES:")
    for db in databases:
        print(f"\t[DB-{databases.index(db)}]:: {str(db).upper()}")
    print()

def choose_db():

    print(f"[QUERY]:: Choose database you want to be connected with (number from 0 to {databases.index(databases[-1])}):")
    while True:
        try:
            query = int(input("\t[INPUT]:: "))
            if query < 0 or query > databases.index(databases[-1]):
                raise ValustatuseError
            break
        except ValueError:
            print("\t[FAIL]:: Invalid number! Try Again")

    try:
        databases[query].db_connect()
        return (query, databases)
    except psycopg2.OperationalError:
        print("[FAIL]:: Can't access database: Wrong user or password")


def active_database(databases):
    for db in databases:
        if db.connected:
            return db

def status(databases):
    db = active_database
    if db:
        return f"[INFO]:: You are connected to {db}"
    else:
        return "You are not connected to any database"


def menu():
    print("\n\n[MENU]::")
    print("\t[OPTION 1]:: view tables")
    print("\t[OPTION 9]:: Choose database")
    print("\t[OPTION 0]:: exit")

    while True:
        try:
            query = int(input('[INPUT]:: '))
            break
        except ValueError:
            print("[FAIL]:: Invalid number! Try Again")
    return query



if __name__ == "__main__":

    option = 9
    while True:
        if option == 0:
            break
        elif option == 9:
            (idx, databases) = setup()
            mdb = databases[idx]
        option = menu()

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
