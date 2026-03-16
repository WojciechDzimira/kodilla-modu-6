CREATE TABLE IF NOT EXISTS Stations (
        station TEXT PRIMARY KEY,  
        latitude FLOAT NOT NULL,
        longitude FLOAT NOT NULL,
        elevation FLOAT NOT NULL,
        name TEXT NOT NULL,
        country TEXT NOT NULL,
        state text not null

    );

    CREATE TABLE IF NOT EXISTS Measurements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        station TEXT NOT NULL,
        date TEXT NOT NULL,
        precip FLOAT,
        tobs FLOAT,
        FOREIGN KEY (station) REFERENCES Stations (station)
    );