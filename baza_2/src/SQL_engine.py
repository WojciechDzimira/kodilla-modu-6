import logging
import sqlite3
from sqlite3 import Error

logging.basicConfig(level=logging.DEBUG)



class DataBaseSQL:
    """Klasa zarzadzająca bazą danych sql"""
    ALLOWED_TABLES = {"Stations", "Measurements"}
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

    def get_table_columns(self, table_name):
        if table_name not in self.ALLOWED_TABLES:
            logging.error(f"Niebezpieczna lub błędna nazwa tabeli: {table_name}")
            return []
        cur = self.conn.cursor()
        cur.execute(f"PRAGMA table_info({table_name})")
        return {row[1] for row in cur.fetchall()}

    def execute_script(self, sql_script_file):
        """Metoda pozwala wykonać skrypt zapisany w pliku"""
        try:
            with open(sql_script_file, "r", encoding="utf-8") as f:
                sql_script = f.read()

            if self.conn:
                cur = self.conn.cursor()
                cur.executescript(sql_script)
                self.conn.commit()
                logging.debug("Wykonano skrypt SQL.")
                return True
            
        except (Error, FileNotFoundError) as e:
            logging.error(f"Błąd wykonania skryptu: {e}")
            return False

    def execute_sql(self, sql, params=()):
        """Metoda wykonuje polecenie sql z paramterami."""
        if self.conn:
            try:
                cur = self.conn.cursor()
                cur.execute(sql, params)          
                self.conn.commit()
                logging.debug("Wykonano polecenie SQL.")
                return cur.fetchall()
            except Error as e:
                logging.error(f"Błąd wykonania SQL: {e}")
    
    def execute_sql_without_commit(self, sql, params=()):
        """Metoda wykonuje polecenie sql z paramterami."""
        if self.conn:
            try:
                cur = self.conn.cursor()
                cur.execute(sql, params)          
            except Error as e:
                logging.error(f"Błąd wykonania SQL: {e}")
                return False # zwraca false jesli blad danych
            return cur.lastrowid

    def select_all(self, table_name):
        """Metoda zwraca wszystkie rekordy z podanej tabeli."""
        if table_name not in self.ALLOWED_TABLES:
            logging.error(f"Niebezpieczna lub błędna nazwa tabeli: {table_name}")
            return []

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
        if table_name not in self.ALLOWED_TABLES:
            logging.error(f"Niebezpieczna lub błędna nazwa tabeli: {table_name}")
            return []
        
        valid_columns = self.get_table_columns(table_name)
        if select_item not in valid_columns:
            logging.error(f"Nieprawidłowa kolumna: {select_item}")
            return []
        
        if self.conn:
            try:
                cur = self.conn.cursor()
                cur.execute(f"SELECT {select_item} FROM {table_name}")
                return cur.fetchall()
            except Error as e:
                logging.error(f"Błąd SELECT: {e}")
        return []                         
    
    def update(self, table_name, column_name, new_value, row_id):
        """Metoda zmienia wartość w określonym miejscu bazy danych"""
        if table_name not in self.ALLOWED_TABLES:
            logging.error(f"Niebezpieczna lub błędna nazwa tabeli: {table_name}")
            return []
        
        valid_columns = self.get_table_columns(table_name)
        if column_name not in valid_columns:
            logging.error(f"Nieprawidłowa kolumna: {column_name}")
            return []
        
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
        if table_name not in self.ALLOWED_TABLES:
            logging.error("Niebezpieczna lub błędna nazwa tabeli: {table_name}")
            return []
        if self.conn:
            try:
                cur = self.conn.cursor()
                sql = f"DELETE FROM {table_name} WHERE id = ?"
                cur.execute(sql, (row_id,)) 
                logging.debug(f"usunięto: wiersz {row_id,} w tabeli {table_name}")
                self.conn.commit()
                
            except Error as e:
                logging.error(f"Błąd Usunięcia: {e}")

    def close(self):
        """metoda zamyka połaczenie z bazą danych"""
        if self.conn:
            self.conn.close()
            self.conn = None