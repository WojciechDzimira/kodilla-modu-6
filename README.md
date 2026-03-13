# 🎬 Movie Library Manager

Projekt osobistej biblioteki filmów i seriali zrealizowany w ramach nauki programowania obiektowego oraz modularyzacji kodu w Pythonie.

## 🚀 Główne funkcjonalności
- **Hybrydowa baza danych**: Obsługa filmów oraz seriali (z podziałem na sezony i odcinki).
- **Zapis i odczyt (JSON)**: Automatyczne zapisywanie stanu biblioteki i wczytywanie jej przy starcie.
- **Generator danych**: Wypełnianie biblioteki realistycznymi tytułami przy użyciu biblioteki `Faker`.
- **System statystyk**: Generowanie losowych wyświetleń i rankingi najpopularniejszych tytułów.
- **Wyszukiwarka**: Możliwość znalezienia konkretnego tytułu w bazie danych.

## 📁 Struktura plików
Program jest podzielony na moduły, co ułatwia zarządzanie kodem:
- `main.py` – Główny punkt wejścia, sterowanie przepływem programu i menu.
- `src/models.py` – Definicje klas (klasa bazowa `Title` oraz klasy `Film` i `Serial`).
- `src/library` – Definicje klay Library
- `utils/utils.py` – Funkcje pomocnicze, walidacja danych (np. `int_input`) W
-
