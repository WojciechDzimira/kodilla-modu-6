import sqlite3
from sqlite3 import Error
import logging
from faker import Faker
fake = Faker('pl_PL')
from utils.utils import int_input, choice
from utils.media_maker import media_maker
from src.SQL_engine import DataBaseSQL
logging.basicConfig(level=logging.DEBUG)



   
if __name__ == '__main__':
    while True:
        base = DataBaseSQL("database.db")
        if choice("Pierwsze uruchomienie? Jeśli chcesz utworzyć losową bazę danych wciśnij: (T) "):
            
            
            base.execute_script("sql_create.sql")
            logging.debug("Utworzono baze danych")

        if choice("chcesz utworzyć filmy? Wciśnij (T):"):
            media = "Movie"
            media_number = int_input("Podaj ile losowych filmów chcesz mieć w bibliotece? Wpisz liczbę całkowitą lub 0:")
            media_maker(base, media, media_number)

        if choice("chcesz utworzyć seriale? Wciśnij (T):"):
            media_number = int_input("Podaj ile losowych seriali ma znaleźć się w bibliotece: kazdy bedzie miał 3 sezony po 15 odcinków. Wpisz liczbę całkowitą lub 0: ")
            media = "Serial"
            media_maker(base, media, media_number)



        

        

        
        if base.conn is None:
            print("Nie udało się połączyć z bazą. Koniec programu.")
            exit(1)
        # Zamknięcie połączenia
        
        if not choice("Ponownie? (T/n): "):
            break
        base.close()
        logging.debug("Zamknięto połączenie z bazą danych")
