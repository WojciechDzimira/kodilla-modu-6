import logging
import random
from .models import Title, Film, Serial
from faker import Faker
fake = Faker('pl_PL')
logging.basicConfig(level=logging.DEBUG)



class Library:
    """ klasa reprezentująca biblioteke """
    def __init__(self):
        self.library = []
    def get_movies(self):
        """funkcja filtruje listę i zwraca tylko filmy"""
        film_list = []
        for record in self.library:
            if isinstance(record, Film):
                film_list.append(record)
        return sorted(film_list, key=lambda x: x.title)
    
    def get_serials(self):
        """funkcja filtruje liste i zwraca tylko seriale"""
        serial_list = []
        for record in self.library:
            if isinstance(record, Serial):
                serial_list.append(record)
        return sorted(serial_list, key=lambda x: x.title)




    def generate_views(self):
        """funkcja wybiera element z biblioteki i dodaje mu losowe wyświetlenia w zakresie od 1 do 100"""
        record = random.randrange(len(self.library))
        self.library[record].views_number += random.randint(1, 100)
    
    def use_generate_views(self):
        """funkcja uruchamia funkcje generate_views() 10 razy"""
        for _ in range(10):
            self.generate_views()


    def top_titles(self, content_type, top_views):
        """funkcja zwraca wybraną ilość najpopularniejszych tytułów w bibliotece"""
        top_views_list = []
        top_views_list = sorted(self.library, key=lambda x: x.views_number, reverse=True)
        

        if content_type == 1:  
            filtered = []
            for record in top_views_list:
                if isinstance(record, Film):
                    filtered.append(record)
            return filtered[:top_views]
        
        
        elif content_type == 2:  
            filtered = []
            for record in top_views_list:
                if isinstance(record, Serial):
                    filtered.append(record)
            return filtered[:top_views]
        
        elif content_type == 3:  
            return top_views_list[:top_views]
        
    


    def episode_number(self, serial_title):
        """funkcja wyświetla liczbę dostępnych odcinków serialu"""
        filtered = []
        for record in self.library:
            if record.title == serial_title:
                filtered.append(record)
        return len(filtered)

    def add_serial_season(self, title, year, genre, views_number, season_number):
        """Funkcja dodaje cały sezon serialu"""
        
        for episode in range(1, 16):
            serial = Serial(
            title = title, 
            year = year,
            genre = genre,
            views_number = views_number,
            season_number = season_number,
            episode_number = episode
            )
            self.library.append(serial)

    def populate_library(self, number_of_films, number_of_serials):
        """funkcja wypełnia biblioteke losowymi danymi filmów i seriali używając faker"""

        genre_list = ["dramaty", "komedia", "tragedia", "fantasy", "horror", "przygodowy", "Sci-fi", "akcja"]
        if number_of_films > 0:
            for i in range(number_of_films):
                film = Film(
                title = fake.catch_phrase(),
                year = fake.year(),
                genre = fake.random_element(genre_list), 
                views_number = 0
                )
                self.library.append(film)
        
        if number_of_serials > 0:
            for i in range(number_of_serials):
                title = fake.catch_phrase()
                year = fake.year()
                genre = fake.random_element(genre_list) 
                views_number = 0
                for season in range(1, 4):
                    self.add_serial_season(title, year, genre, views_number, season)
            return self.library
    
    def search(self, text):
        """funkcja wyszukuje film lub serial po jego tytule"""
        text = text.lower()
        for record in self.library:
            if text == record.title.lower():
                return record
            
        logging.debug("Brak wyszukiwanego tytułu w bibliotece")
        logging.warning("Użytkownik próbował wyszukać tytuł którego nie ma w bibliotece")
        return None

    def library_to_dicts(self):
        """Funkcja konwertuje listę obiektów Film/Serial na listę słowników"""
        result = []   
        for i, record in enumerate(self.library, start=1): 
            rekord_dict = {   
                "record_id" : i,            
                "type": "Film" if isinstance(record, Film) else "Serial",  
                "title": record.title,
                "year": record.year,
                "genre": record.genre,
                "views": record.views_number,
            }
            if isinstance(record, Serial):
                rekord_dict["episode_number"] = record.episode_number
                rekord_dict["season_number"] = record.season_number
            
            result.append(rekord_dict) 
        
        return result    
    def load_from_json(self, library_dict):
        """Funkcja odczytuje plik biblioteka.json i zamienia go na liste obiektów"""
        self.library = []
        for record in library_dict:
            if record["type"] == "Film":
                film = Film(
                title = record["title"],
                year = record["year"],
                genre = record["genre"], 
                views_number = record["views"]
                )
                self.library.append(film)
            else:
                serial = Serial(
                title = record["title"],
                year = record["year"],
                genre = record["genre"], 
                views_number = record["views"],
                episode_number = record["episode_number"],
                season_number = record["season_number"]
                )
                self.library.append(serial)