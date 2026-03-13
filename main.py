import logging
import json
from datetime import datetime
logging.basicConfig(level=logging.DEBUG)
from utils.utils import int_input, choose_content_type
from src.library import Library
from src.models import Film, Serial



while True:
    if __name__ == "__main__":  
        today_datetime = datetime.now().strftime("%d.%m.%Y")
        library_list = Library()
        
        

        while  True:
            x = int_input("Wczytać istniejącą listę: wpisz 1, utworzyc nową losową listę: wpisz 2 ")
            if x == 1:
                with open("biblioteka.json", "r", encoding="utf-8") as f:
                    library_dict = json.load(f)
                    logging.debug(f"wczytano plik bibliotek.json i przekazano tam dane z library_dict")
                library_list.load_from_json(library_dict)
                break
            if x == 2:
                print("UZUPEŁNIANIE BIBLIOTEKI LOSOWYMI FILMAMI/SERIALAMI")
                number_of_films = int_input("Podaj ile losowych filmów chcesz mieć w bibliotece? Wpisz liczbę całkowitą lub 0: ")
                number_of_serials = int_input("Podaj ile losowych seriali ma znaleźć się w bibliotece: kazdy bedzie miał 3 sezony po 15 odcinków. Wpisz liczbę całkowitą lub 0: ")
                library_list.populate_library(number_of_films, number_of_serials)
                library_dict = library_list.library_to_dicts()
                break


        library_list.use_generate_views()
        
        print(f"Najpopularniejsze filmy i seriale dnia {today_datetime}: ")
        content_type = choose_content_type()
        top_views = int_input("Jaką liczbę najpopularniejszych tytułów wyświetlić? Podaj liczbę całkowotą większą od 0: ")
        top = library_list.top_titles(content_type, top_views)
        for i, record in enumerate (top, start=1):
            if isinstance(record, Film):
                print(f"nr{i}: {record.title}, liczba wyświetleń {record.views_number}")
            else:
                print(f"nr{i}: {record.title}, S{record.season_number:02d}E{record.episode_number:02d} liczba wyświetleń {record.views_number}")
        
        library_dict = library_list.library_to_dicts() 
        with open("biblioteka.json", "w", encoding="utf-8") as record:
                json.dump(library_dict, record, ensure_ascii=False, indent=4)
                logging.debug(f"utworzono plik bibliotek.json i przekazano tam dane z library_dict")

    choice = input("Ponownie? (T/n): ").lower()
    if choice != "t":
        break