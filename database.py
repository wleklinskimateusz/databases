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
        print(f"[DB-{databases.index(db)}]:: {str(db).upper()}")
    print()

    print(f"[QUERY]:: Choose database you want to be connected with (number from 0 to {databases.index(databases[-1])}):")
    while True:
        try:
            query = int(input("[INPUT]:: "))
            if query < 0 or query > databases.index(databases[-1]):
                raise ValueError
            break
        except ValueError:
            print("[FAIL]:: Invalid number! Try Again")

    databases[query].db_connect()
    return (query, databases)


def menu():
    print("[MENU]::")
    print("\t[OPTION 1]:: view tables")

    while True:
        try:
            query = int(input('[INPUT]:: '))
            break
        except ValueError:
            print("[FAIL]:: Invalid number! Try Again")
    return query



if __name__ == "__main__":

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
