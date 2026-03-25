import sqlite3
from sqlite3 import Error
import logging
import csv 
from pathlib import Path
from src.SQL_engine import DataBaseSQL
from utils.data_manager import *
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    db_file = "database.db"
    file_path = Path(db_file)
    
    
    base = DataBaseSQL("database.db") 
    while True:
        db_exist = file_path.exists()
        
        if base.conn is None:
            print("Nie udało się połączyć z bazą. Koniec programu.")
            logging.error("Błąd połączenia z bazą danych")
            exit(1)

        
        if db_exist:
            if not choice(f"Plik bazy danych: {db_file} już istnieje. Czy na pewno chcesz kontynuować i ewentualnie nadpisać dane? (t/n): "):
                print("Anulowano import danych")
            else:
                data_base_creation(base)
        else:
            data_base_creation(base)
        
        if choice("Czy chcesz wyświetlić top 3 temperatury ze wszystkich stacji? Wpisz (t) "):
            top_temp_in_stations(base)
        
        if not choice("Ponownie? (T/n): "):
            break
    base.close()
    logging.debug("Zamknięto połączenie z bazą danych")
  
