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


if __name__ == "__main__":
    databases = write_db()
