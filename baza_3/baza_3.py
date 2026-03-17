import sqlite3
from sqlite3 import Error
import logging
from faker import Faker
fake = Faker('pl_PL')
from utils.utils import int_input, choose_content_type, choice
from src.SQL_engine import DataBaseSQL

logging.basicConfig(level=logging.DEBUG)


   

def data_base_creation(base):
    
    base.execute_script("sql_create.sql")


def populate(base):
  
    while  True:
        genre_list = ["dramaty", "komedia", "tragedia", "fantasy", "horror", "przygodowy", "Sci-fi", "akcja"]
        x = int_input("Wczytać istniejącą listę: wpisz 1, utworzyc nową losową listę: wpisz 2 ")
        if x == 1:
            print("jeszcze mnie tu nie ma, ale bede ")

        if x == 2:
            print("UZUPEŁNIANIE BIBLIOTEKI LOSOWYMI FILMAMI/SERIALAMI")
            number_of_films = int_input("Podaj ile losowych filmów chcesz mieć w bibliotece? Wpisz liczbę całkowitą lub 0: ")
            number_of_serials = int_input("Podaj ile losowych seriali ma znaleźć się w bibliotece: kazdy bedzie miał 3 sezony po 15 odcinków. Wpisz liczbę całkowitą lub 0: ")
            
            





def media_maker(base, media, media_number):
    genre_list = [
    "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", "History", 
    "Horror", "Music", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]

    sql = "INSERT INTO Media (title, release_year, director, genre, content_type) VALUES (?, ?, ?, ?, ?)"
    for x in range(media_number):
                
        title = fake.catch_phrase()
        release_year = fake.year()
        director = fake.name()
        genre = fake.random_element(genre_list)
        content_type = media
        row = (title, release_year, director, genre, content_type)
        row_id  = base.execute_sql_without_commit(sql, row)

        if media == "Movie":
            sql_movie = "INSERT INTO Movies (id) VALUES (?)"
            base.execute_sql_without_commit(sql_movie, (row_id,))

        elif media == "Serial":
            sql_serial = "INSERT INTO Episodes (media_id, season_number, episode_number) VALUES (?, ?, ?)"
            for season in range(1, 4):
                for episode in range(1, 16):
                    base.execute_sql_without_commit(sql_serial, (row_id, season, episode))
    base.conn.commit()
   








if __name__ == '__main__':
    while True:
        
        if choice("Pierwsze uruchomienie? Jeśli chcesz utworzyć losową bazę danych wciśnij: (T) "):
            
            base = DataBaseSQL("database.db")
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
        base.close()
        logging.debug("Zamknięto połączenie z bazą danych")

        if not choice("Ponownie? (T/n): "):
            break