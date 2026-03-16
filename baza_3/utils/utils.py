import logging
def int_input(text):
    """Funkcja prosi uzytkownika o liczbę całkowitą i sprawdza czy 
    uzytkownik faktycznie wprowadził liczbę calkowita"""
    while True:
        try:
            number = int(input(f"{text}"))
            if number > -1:
                return number
            else:
                print("to nie jest dodatnia liczba całkowita, wprowadz jeszcze raz.")
                logging.warning("Użytkownik wprowadził liczbę ujemną")
        except ValueError:
            print("to nie jest liczba całkowita, wprowadz jeszcze raz.")
            logging.warning("Użytkownik wprowadził wartośc nie będącą liczbą")


def choose_content_type():
        """"Funkcja wyboru rodzaju wyświetlanych najpopularniejszych tytułów z biblioteki"""
        print("1: Najpopularniejsze Filmy \n2: Najpopularniejsze Seriale \n3: Najpopularniejsze Ogólnie")
        while True:
            choice = int_input("Wpisz 1, 2 lub 3: ")
            if choice  in {1, 2, 3}:
                return choice
            else:
                print("Błąd, wpisz jeszcze raz")  
                logging.warning("Użytkownik wprowadził niepoprawną wartość") 

def choice(text):
    if input(f"{text}") == "t":
        return True
    return False


