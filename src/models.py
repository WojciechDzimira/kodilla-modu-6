import logging
class Title:
    """klasa reprezentująca rekord biblioteki"""
    def __init__(self, title, year, genre, views_number):
        self.title = title
        self.year = year
        self.genre = genre
        self.views_number = views_number

class Film(Title):
    """ klasa reprezentująca filmy, dziedzicząca po klasie Title """
    def __init__(self, title, year, genre, views_number):
        super().__init__(
            title = title, 
            year = year, 
            genre = genre,
            views_number = views_number)
        logging.debug(f"Do biblioteki dodano film {title} {year}")
    def play(self):
        """metoda wyświetla tytuł i rok wydania filmu oraz dodaje 1 do odtworzeń"""
        print(f"{self.title} {self.year}.")
        self.views_number += 1

class Serial(Title):
    """ klasa reprezentująca seriale, dziedzicząca po klasie Title """
    def __init__(self, title, year, genre, views_number, episode_number, season_number):
        super().__init__(
            title = title, 
            year = year, 
            genre = genre,
            views_number = views_number
        )
        self.episode_number = episode_number
        self.season_number = season_number
        logging.debug(f"Rozszerzono bibliotekę o serial: {title}, S:{self.season_number:02d}, E:{self.episode_number:02d}")
    def play(self):
        """metoda wyświetla tytuł numer sezonu i nr odcinka oraz dodaje 1 do odtworzeń"""
        print(f"{self.title} S{self.season_number:02d} E{self.episode_number:02d}.")
        self.views_number += 1