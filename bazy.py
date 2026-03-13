import sqlite3
from sqlite3 import Error
import logging

logging.basicConfig(level=logging.DEBUG)

class DataBaseSQL:
    """Klasa zarzadzająca bazą danych sql"""

    def __init__(self, db_file):
        self.conn = self.create_connection(db_file)

    def create_connection(self, db_file):
        """Tworzy połączenie z bazą danych"""
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            logging.debug(f"Połączono z {db_file}")
            return conn
        except Error as e:
            logging.error(f"Błąd połączenia z bazą: {e}")
        return conn

    def execute_script(self, sql_script_file):
        """Metoda pozwala wykonać skrypt zapisany w pliku"""
        with open(sql_script_file, "r", encoding="utf-8") as f:
            sql_script = f.read()
        if self.conn:
            try:
                cur = self.conn.cursor()
                cur.executescript(sql_script)
                self.conn.commit()
                logging.debug("Wykonano skrypt SQL.")
            except Error as e:
                logging.error(f"Błąd wykonania skryptu: {e}")

    def execute_sql(self, sql, params=()):
        """Metoda wykonuje polecenie sql z paramterami."""
        if self.conn:
            try:
                cur = self.conn.cursor()
                cur.execute(sql, params)          
                self.conn.commit()                
                logging.debug("Wykonano SQL i zatwierdzono zmiany.")
            except Error as e:
                logging.error(f"Błąd wykonania SQL: {e}")

    def select_all(self, table_name):
        """Metoda zwraca wszystkie rekordy z podanej tabeli."""
        if self.conn:
            try:
                cur = self.conn.cursor()
                cur.execute(f"SELECT * FROM {table_name}")
                return cur.fetchall()
            except Error as e:
                logging.error(f"Błąd SELECT: {e}")
        return []                         
    
    def select(self, select_item, table_name):
        """Metoda zwraca coś z podanej tabeli"""
        if self.conn:
            try:
                cur = self.conn.cursor()
                cur.execute(f"SELECT {select_item} FROM {table_name}")
                return cur.fetchall()
            except Error as e:
                logging.error(f"Błąd SELECT: {e}")
        return []                         
    
    def select_tasks_by_project(self, project_id):
        """Metoda zwraca zadania dla danego projektu."""
        if self.conn:
            try:
                cur = self.conn.cursor()
                cur.execute("SELECT * FROM Zadanie WHERE projekt_id = ?", (project_id,)) 
                return cur.fetchall()
            except Error as e:
                logging.error(f"Błąd SELECT zadań: {e}")
        return []

    def update(self, table_name, column_name, new_value, row_id):
        """Metoda zmienia wartość w określonym miejscu bazy danych"""
        if self.conn:
            try:
                cur = self.conn.cursor()
                sql = f"UPDATE {table_name} SET {column_name} = ? WHERE id = ?"
                cur.execute(sql, (new_value, row_id)) 
                logging.debug(f"Zaktualizowano: tabele {table_name} w wierszu {row_id}")
                self.conn.commit()
            except Error as e:
                logging.error(f"Błąd Update: {e}")

    def delete(self, table_name, row_id):
        """metoda usuwa określony element bazy danych"""
        if self.conn:
            try:
                cur = self.conn.cursor()
                sql = f"DELETE FROM {table_name} WHERE id = ?"
                cur.execute(sql, (row_id,)) 
                logging.debug(f"usunięto: wiersz {row_id,} w tabeli {table_name}")
                self.conn.commit()
                
            except Error as e:
                logging.error(f"Błąd Usunięcia: {e}")

    def add_project(self, project):
        """Metoda tworzy nowy projekt"""
        if self.conn:
            sql = '''INSERT INTO Projekt (nazwa, start_date, end_date)
                    VALUES (?, ?, ?)'''
            try:
                cur = self.conn.cursor()
                cur.execute(sql, project)
                self.conn.commit()
                return cur.lastrowid
            except Error as e:
                logging.error(f"Błąd dodawania projektu: {e}")
        return None

    def add_task(self, task):
        """Metoda dodaje nowe zadanie."""
        if self.conn:
            sql = '''INSERT INTO Zadanie (projekt_id, nazwa, opis, status, start_date, end_date)
                    VALUES (?, ?, ?, ?, ?, ?)'''
            try:
                cur = self.conn.cursor()
                cur.execute(sql, task)
                self.conn.commit()
                return cur.lastrowid
            except Error as e:
                logging.error(f"Błąd dodawania zadania: {e}")
        return None

    def close(self):
        """metoda zamyka połaczenie z bazą danych"""
        if self.conn:
            self.conn.close()

    def test_data(self):
        """metoda wykozystuje pliki sql do utworzenia danych testowych"""
        self.execute_script("sql_create.sql")
        self.execute_script("sql_test_data.sql")
        projects = base.select_all("Projekt")
        for project in projects:
            project_id = project[0]
            project_start = project[2]     
            project_end = project[3]        
            for i in range (1,3):
                task=(              project_id,
                                    f"Zadanie {i}",
                                    f"Zrób skrypt{i}",
                                    "Do zrobienia", 
                                    project_start, 
                                    project_end)
                base.add_task(task) 

def show_project(base):
    """funkcja wyświetla tabele Projekty"""
    projekt_list = base.select_all("Projekt")
    for projekt in projekt_list:
        print(projekt)
def show_tasks(base):
    """funkcja wyświetla tabele Zadania"""
    zadanie_list = base.select_all("Zadanie")
    print("\n--- Zadania ---")
    for zadanie in zadanie_list:
        print(f"ID zadania: {zadanie[0]}, ID projektu: {zadanie[1]}, Treść zadania: {zadanie[2]}, Status: {zadanie[4]}, data Rozpoczęcia: {zadanie[5]}, data zakonczenia: {zadanie[6]}")
    


if __name__ == '__main__':
    base = DataBaseSQL("database.db")
    if base.conn is None:
        print("Nie udało się połączyć z bazą. Koniec programu.")
        exit(1)

    # Tworzenie tabel
    base.test_data()

    # Wyświetlanie projektów
    print("Projekty--------")
    show_project(base)

    # Wyświetlanie zadań
    print("Zadania---------")
    show_tasks(base)

    #Zmiana bazy
    print("UPDATE-----------")
    base.update("Projekt", "start_date", "Tutaj jest zmiana", 3)
    show_project(base)
    
    print("DELETE-----------")
    base.delete("Projekt", 3)
    show_project(base)

    # Zamknięcie połączenia
    base.close()
