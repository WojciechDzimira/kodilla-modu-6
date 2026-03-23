import sqlite3
from sqlite3 import Error
import logging
import csv 
from pathlib import Path
from SQL_engine import DataBaseSQL
logging.basicConfig(level=logging.DEBUG)


def import_from_csv(base, table_name, file_path):
    ALLOWED_TABLES = {"Stations", "Measurements"}
    ALLOWED_COLUMNS = {"station", "date", "precip", "tobs" ,"latitude", "longitude", "elevation", "name", "country", "state"}

    if table_name not in ALLOWED_TABLES:
            logging.error(f"Niebezpieczna lub błędna nazwa tabeli: {table_name} w pliku {file_path}")
            return []

    with open(file_path, mode='r', encoding='utf-8') as f:

        reader = csv.DictReader(f)
        columns = reader.fieldnames

        if not set(columns).issubset(ALLOWED_COLUMNS):
            logging.error(f"Niebezpieczna lub błędna nazwa kolumny w pliku csv {file_path}")
            return []   
        
        placeholders = ", ".join(["?"] * len(columns))
        row_counter = 0
        success_counter = 0
        sql = f"INSERT OR IGNORE INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            
        for row in reader:
            row_counter += 1
            if  base.execute_sql_without_commit(sql, tuple(row.values())):
                success_counter +=1
            else: 
                logging.error(f"Błąd danych w wierszu {row_counter}")
                
                
        base.conn.commit()
        logging.debug("Wykonano import danych z pliku csv do bazy danych i zatwierdzono zmiany")
        logging.debug(f"Udało się importować {success_counter}/{row_counter} wierszy z pliku {file_path}")

def data_base_creation(base):
    
    base.execute_script("sql_create.sql")
    import_from_csv(base, "Stations", "clean_stations.csv")
    import_from_csv(base, "Measurements", "clean_measure.csv")


def top_temp_in_stations(base):
    sql = """
            SELECT S.name, M.date, M.tobs 
            FROM Measurements M
            JOIN Stations S ON M.station = S.station 
            WHERE S.station = ? 
            ORDER BY M.tobs DESC 
            LIMIT 3
            """

    print("\n" + "="*70)
    print("Maksymalne temperatury w stacjach (TOP 3)")
    print()
    stations = base.select("station", "Stations")
    for (station_id,) in stations:
        results = base.execute_sql(sql, (station_id,))
        print("\n" + "="*70)
            
        if results:
            print(f"\nSTACJA: {results[0][0]} (ID: {station_id})")
            for _, date, temp in results:
                print(f"  > Dnia {date} odnotowano {temp}°C")

    print("\n" + "="*70)

