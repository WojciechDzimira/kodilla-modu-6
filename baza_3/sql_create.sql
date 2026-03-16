CREATE TABLE IF NOT EXISTS Media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  
    title TEXT NOT NULL,
    release_year TEXT NOT NULL,
    director TEXT NOT NULL,
    genre TEXT NOT NULL,
    views INTEGER DEFAULT 0,
    content_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Movies (
    id INTEGER PRIMARY KEY,
    has_oscar INTEGER DEFAULT 0, 
    FOREIGN KEY (id) REFERENCES Media (id)
);

CREATE TABLE IF NOT EXISTS Episodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    media_id INTEGER NOT NULL,
    season_number INTEGER DEFAULT 1,
    episode_number INTEGER DEFAULT 1,
    FOREIGN KEY (media_id) REFERENCES Media (id)
);