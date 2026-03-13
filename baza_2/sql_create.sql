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