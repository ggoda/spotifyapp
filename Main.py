import sqlite3
import datetime

# given a username and reputation, add the user to the db if the username is unique, otherwise update their reputation.
# returns the userid of the user
def insertUser(username, dailyRep, totalRep):
    data = c.execute('SELECT * FROM user WHERE name LIKE (?)', [username]).fetchall()
    if data:
        c.execute('UPDATE user SET dailyRep=(?) AND totalRep=(?) WHERE name LIKE (?)',
                        [dailyRep, totalRep, username])
        id = data[0]['id']
    else:
        cur = c.execute("INSERT INTO user (name, dailyRep, totalRep) VALUES (?,?, ?)", [username, dailyRep, totalRep])
        id = cur.lastrowid
    conn.commit()
    return id;

# given a song name and unique songid, update the song's last play and rep if it exists or insert the song into the db
# returns the songid of the song
def insertSong(name, id, rep):
    data = c.execute('SELECT * FROM song WHERE name LIKE (?) and id=(?)', [name, id]).fetchall()
    if data:
        c.execute('UPDATE song SET LastPlay = (?) AND rep=(?) WHERE id =(?)', [datetime.datetime.now(), rep, id])
    else:
        c.execute('INSERT INTO song (Name, Rep, LastPlay, Id) VALUES (?, ?, ?, ?)',
                        [name, rep, datetime.datetime.now(), id])
        conn.commit()
    return id;

# given an artist name, insert it into the db if it's unique, otherwise update the artists' rep
# returns the artistid of the artist
def insertArtist(name, rep):
    data = c.execute('SELECT * FROM artist WHERE name LIKE (?)', [name]).fetchall()
    if data:
        id = data[0]['id']
        c.execute('UPDATE artist SET rep = (?) WHERE name =(?)', [rep, name])
    else:
        cur = c.execute('INSERT INTO artist (name, rep) VALUES (?, ?)', [name, rep])
        id = cur.lastrowid
        conn.commit()
    return id

# given an artistid and a songid, add a relationship between the song and the artist
def addArtistSongRelation(artistid, songid):
    data = c.execute('SELECT * FROM artist_song WHERE artistId = (?) AND songId = (?)', [artistid, songid]).fetchall()
    if data:
        return
    else:
        c.execute('INSERT INTO artist_song (artistId, songId) VALUES (?, ?)', [artistid, songid])
        conn.commit()

# given an userid and songid, add a relationship between the user and song with a count of 1 if the relationship is
# new, or update the relationship's lastPlay to now and increment count
def addUserSongRelation(userid, songid):
    data = c.execute('SELECT * FROM user_song WHERE userId = (?) AND songId = (?)', [userid, songid]).fetchall()
    if data:
        count = data[0]['count']
        c.execute('UPDATE user_song SET lastPlay = (?) AND count=(?) WHERE userId = (?) AND songId = (?)',
                  [datetime.datetime.now(), count + 1])
    else:
        c.execute('INSERT INTO user_song (artistId, songId, lastPlay, count) VALUES (?, ?)',
                  [userid, songid, datetime.datetime.now(), 1])
        conn.commit()

# given a username, return the reputation of that user in a list [dailyRep, totalRep] or -1 if the user does not exist
def getUserRep(username):
    data = c.execute('SELECT * FROM user WHERE name LIKE (?)', [username]).fetchall()
    if data:
        return [data[0]['dailyRep'], data[0]['totalRep']]
    else:
        return -1

# given a songid, return the reputation of that song or -1 if the song does not exist
def getSongRep(songid):
    data = c.execute('SELECT * FROM song WHERE id = (?)', [songid]).fetchall()
    if data:
        return data[0]['rep']
    else:
        return -1

# given an artist name, return the reputation of that artist or -1 if the artist does not exist
def getArtistRep(artist):
    data = c.execute('SELECT * FROM artist WHERE name LIKE (?)', [artist]).fetchall()
    if data:
        return data[0]['rep']
    else:
        return -1

# given an artist name, return all songs in the db by that artist
def getArtistSongs(artist):
    # get artist id
    data = c.execute('SELECT * FROM artist WHERE name LIKE (?)', [artist]).fetchall()
    if data:
        # get all songs with that artist id
        data2 = c.execute('SELECT * FROM song s INNER JOIN artist_song a ON a.artistId = ? WHERE s.id = a.songId',
                          [data[0]['id']]).fetchall()
        if data2:
            songs = []
            # add each of the artists' songs to the list
            for d in data2:
                songs.extend([d['name']])
            return songs
        else:
            return False
    else:
        return False

def getUserSongs(username):
    data = c.execute('SELECT * FROM user WHERE name LIKE (?)', [username]).fetchall()
    if data:
        # get all songs with that artist id
        data2 = c.execute('SELECT * FROM song s INNER JOIN user_song u ON u.userId = ? WHERE s.id = u.songId',
                          [data[0]['id']]).fetchall()
        if data2:
            songs = []
            # add each of the artists' songs to the list
            for d in data2:
                songs.extend([d['name']])
            return songs
        else:
            return False
    else:
        return False

# FOR INTERNAL USE ONLY
# makes db calls return a dictionary of results
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
        for idx, value in enumerate(row))

# EXAMPLE FUNCTION: This function shows how to add artists and songs to the db, when adding songs you must also add a
# relation between all of the songs artists
# given a list of artists, a song name, and unique song id, insert all of the artists and the song into the dbs
def insertArtistSong(artists, song, songid):
    artistids = []
    insertSong(song, songid)
    for artist in artists:
        artistids.append(insertArtist(artist))
    for artistid in artistids:
        addRelation(artistid, songid)

conn = sqlite3.connect('song.db')
conn.row_factory = make_dicts
c = conn.cursor()

c.insertUser("wonnor", 15, 10);
c.insertSong("No Type", 10);

