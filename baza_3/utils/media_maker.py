import logging
from faker import Faker
fake = Faker('pl_PL')


def media_maker(base, media, media_number):
    genre_list = [
    "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]

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
            print("hak")
            sql_serial = "INSERT INTO Episodes (media_id, season_number, episode_number) VALUES (?, ?, ?)"
            for season in range(1, 4):
                for episode in range(1, 16):
                    base.execute_sql_without_commit(sql_serial, (row_id, season, episode))
    base.conn.commit()