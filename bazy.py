import sqlite3
from sqlite3 import Error
import logging

logging.basicConfig(level=logging.DEBUG)


def create_connection(db_file):
    """Tworzy połączenie z bazą SQLite. Zwraca obiekt połączenia lub None w razie błędu."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logging.debug(f"Połączono z {db_file}")
        return conn
    except Error as e:
        logging.error(f"Błąd połączenia z bazą: {e}")
    return conn


def execute_sql(conn, sql, params=()):
    """Wykonuje dowolne zapytanie modyfikujące z bezpiecznymi parametrami."""
    try:
        cur = conn.cursor()
        cur.execute(sql, params)          # params jako krotka → chroni przed SQL Injection
        conn.commit()                     # zawsze commit po modyfikacji
        logging.debug("Wykonano SQL i zatwierdzono zmiany.")
    except Error as e:
        logging.error(f"Błąd wykonania SQL: {e}")


def select_all(conn, table_name):
    """Zwraca wszystkie rekordy z tabeli Projekt."""
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        return cur.fetchall()
    except Error as e:
        logging.error(f"Błąd SELECT: {e}")
        return []                         # zawsze zwracamy listę, nigdy None → łatwiej obsługiwać


def select_tasks_by_project(conn, project_id):
    """Zwraca zadania dla danego projektu (bezpieczne zapytanie z parametrem)."""
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Zadanie WHERE projekt_id = ?", (project_id,))  # krotka z jednym elementem!
        return cur.fetchall()
    except Error as e:
        logging.error(f"Błąd SELECT zadań: {e}")
        return []

def update_task(conn, table_name, new_status, task_id):
    try:
        cur = conn.cursor()
        cur.execute(f"UPDATE {table_name} SET status = ? WHERE id = ?", (new_status, task_id))  
        conn.commit()
    except Error as e:
        logging.error(f"Błąd Update zadania: {e}")
        
        return []
def add_project(conn, project):
    """
    Dodaje nowy projekt.
    project = (nazwa, start_date, end_date)
    Zwraca nowe ID lub None w razie błędu.
    """
    try:
        cur = conn.cursor()
        
        # 1. Sprawdzamy, czy projekt o takiej nazwie już istnieje
        cur.execute("SELECT id FROM Projekt WHERE nazwa = ?", (project[0],))
        istniejacy_projekt = cur.fetchone()
        
        if istniejacy_projekt:
            logging.info(f"Projekt o nazwie '{project[0]}' już istnieje (ID: {istniejacy_projekt[0]}). Pomijam.")
            return istniejacy_projekt[0]  # zwracamy ID istniejącego projektu

        # 2. Jeśli nie istnieje, dodajemy nowy
        sql = '''INSERT INTO Projekt (nazwa, start_date, end_date)
                 VALUES (?, ?, ?)'''
        cur.execute(sql, project)
        conn.commit()
        logging.info(f"Dodano nowy projekt: '{project[0]}'")
        return cur.lastrowid
    except Error as e:
        logging.error(f"Błąd dodawania projektu: {e}")
        return None


def add_task(conn, task):
    """
    Dodaje nowe zadanie.
    task = (projekt_id, nazwa, opis, status, start_date, end_date)
    Zwraca nowe ID lub None.
    """
    try:
        cur = conn.cursor()
        
        # 1. Sprawdzamy, czy zadanie o takiej nazwie już w tym projekcie istnieje
        cur.execute("SELECT id FROM Zadanie WHERE projekt_id = ? AND nazwa = ?", (task[0], task[1]))
        istniejace_zadanie = cur.fetchone()
        
        if istniejace_zadanie:
            logging.info(f"Zadanie '{task[1]}' w projekcie ID {task[0]} już istnieje. Pomijam.")
            return istniejace_zadanie[0]

        # 2. Jeśli nie istnieje, dodajemy
        sql = '''INSERT INTO Zadanie (projekt_id, nazwa, opis, status, start_date, end_date)
                 VALUES (?, ?, ?, ?, ?, ?)'''
        cur.execute(sql, task)
        conn.commit()
        logging.info(f"Dodano nowe zadanie: '{task[1]}'")
        return cur.lastrowid
    except Error as e:
        logging.error(f"Błąd dodawania zadania: {e}")
        return None


if __name__ == '__main__':
    connection = create_connection("database.db")

    if connection is None:
        print("Nie udało się połączyć z bazą. Koniec programu.")
        exit(1)

    # Tworzenie tabel – bez INSERT-ów w CREATE (lepiej osobno dodawać dane)
    sql_create = """
    CREATE TABLE IF NOT EXISTS Projekt (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        nazwa TEXT NOT NULL,
        start_date TEXT,
        end_date TEXT
    );

    CREATE TABLE IF NOT EXISTS Zadanie (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        projekt_id INTEGER,
        nazwa TEXT NOT NULL,
        opis TEXT,
        status TEXT,
        start_date TEXT,
        end_date TEXT,
        FOREIGN KEY (projekt_id) REFERENCES Projekt (id)
    );
    """

    # Wykonanie tworzenia tabel
    try:
        cursor = connection.cursor()
        cursor.executescript(sql_create)

        add_project(connection, ("Szkola", "10.12.2026", "15.12.2026"))
        add_project(connection, ("Dom", "12.12.2026", "16.12.2026"))
        add_project(connection, ("Sklep", "13.12.2026", "17.12.2026"))
        add_project(connection, ("Salon", "14.12.2026", "18.12.2026"))
        task = (1, "Zadanie do domu ", "opis zadania ", "Do wykonania ", "12.10.2026", "15.10.2026")
        add_task(connection, task)
        #update_task(connection, "Zadanie", "robione test", 3)
        connection.commit()
    except Error as e:
        logging.error(f"Błąd tworzenia tabel: {e}")
        connection.close()
        exit(1)
    projekt_list = select_all(connection, "Projekt")
    for projekt in projekt_list:
        print(projekt)
    projekt_list = select_all(connection, "Zadanie")
    for projekt in projekt_list:
        print(f"ID zadania: {projekt[0]}, ID projektu: {projekt[1]},Treść zadania: {projekt[2]},Status: {projekt[4]},data Rozpoczęcia: {projekt[5]}, data zakonczenia: {projekt[6]}")
    connection.close()