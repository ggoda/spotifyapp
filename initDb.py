__author__ = 'asteere'

import sqlite3
conn = sqlite3.connect('song.db')

c = conn.cursor()

c.execute('''CREATE TABLE artist
             (name TEXT NOT NULL, rep INTEGER NOT NULL, id INTEGER PRIMARY KEY)''')

c.execute('''CREATE TABLE song
             (name TEXT NOT NULL, rep INTEGER NOT NULL, lastPlay timestamp, id INTEGER PRIMARY KEY)''')

c.execute('''CREATE TABLE user
             (name TEXT NOT NULL, dailyRep INTEGER NOT NULL, totalRep INTEGER NOT NULL, id INTEGER PRIMARY KEY)''')

c.execute('''CREATE TABLE artist_song
             (artistId INTEGER, songId INTEGER,
             FOREIGN KEY(artistId) REFERENCES artist(id), FOREIGN KEY(songId) REFERENCES song(id))''')

c.execute('''CREATE TABLE user_song
             (userId INTEGER, songId INTEGER, lastPlay timestamp, count INTEGER NOT NULL,
             FOREIGN KEY(userId) REFERENCES user(id), FOREIGN KEY(songId) REFERENCES song(id))''')

conn.commit()

conn.close()
