import sqlite3
import datetime


# given a username and reputation, add the user to the db if the username is unique, otherwise update their reputation.
# returns the userid of the user
def insertUser(username, dailyRep, totalRep):
    data = c.execute('SELECT * FROM user WHERE name LIKE (?)', [username]).fetchall()
    if data:
        c.execute('UPDATE user SET dailyRep=(?), totalRep=(?) WHERE name LIKE (?)',
                  [dailyRep, totalRep, username])
        id = data[0]['id']
    else:
        cur = c.execute("INSERT INTO user (name, dailyRep, totalRep) VALUES (?,?, ?)", [username, dailyRep, totalRep])
        id = cur.lastrowid
    conn.commit()
    return id

# given a song name and unique songid, update the song's last play and rep if it exists or insert the song into the db
# returns the songid of the song
def insertSong(name, id, rep):
    data = c.execute('SELECT * FROM song WHERE name LIKE (?) and id=(?)', [name, id]).fetchall()
    if data:
        c.execute('UPDATE song SET LastPlay = (?), rep=(?) WHERE id =(?)', [datetime.datetime.now(), rep, id])
    else:
        c.execute('INSERT INTO song (Name, Rep, LastPlay, Id) VALUES (?, ?, ?, ?)',
                        [name, rep, datetime.datetime.now(), id])
        conn.commit()
    return id

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
        c.execute('UPDATE user_song SET lastPlay = (?), count=(?) WHERE userId = (?) AND songId = (?)',
                  [datetime.datetime.now(), count + 1, userid, songid])
    else:
        c.execute('INSERT INTO user_song (userId, songId, lastPlay, count) VALUES (?, ?, ?, ?)',
                  [userid, songid, datetime.datetime.now(), 1])
        conn.commit()

# given a username, return the reputation of that user in a list [dailyRep, totalRep] or false if the user does not exist
def getUserRep(username):
    data = c.execute('SELECT * FROM user WHERE name LIKE (?)', [username]).fetchall()
    if data:
        return [data[0]['dailyRep'], data[0]['totalRep']]
    else:
        return False

# given a songid, return the reputation of that song or false if the song does not exist
def getSongRep(songid):
    data = c.execute('SELECT * FROM song WHERE id = (?)', [songid]).fetchall()
    if data:
        return data[0]['rep']
    else:
        return False

# given an artist name, return the reputation of that artist or false if the artist does not exist
def getArtistRep(artist):
    data = c.execute('SELECT * FROM artist WHERE name LIKE (?)', [artist]).fetchall()
    if data:
        return data[0]['rep']
    else:
        return False

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

# given a username returns a list of dictionaries, each dictionary representing a song played by the user
def getUserSongs(username):
    data = c.execute('SELECT * FROM user WHERE name LIKE (?)', [username]).fetchall()
    if data:
        # get all songs with that artist id
        data2 = c.execute('SELECT * FROM song s INNER JOIN user_song u ON u.userId = ? WHERE s.id = u.songId',
                          [data[0]['id']]).fetchall()
        if data2:
            return data2
        else:
            return False
    else:
        return False

# FOR INTERNAL USE ONLY
# makes db calls return a list of dictionaries instead of random shit
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
        for idx, value in enumerate(row))

# EXAMPLE FUNCTION: This function shows how to add artists and songs to the db, when adding songs you must also add a
# relation between all of the songs artists
# given a list of artists, a song name, and unique song id, insert all of the artists and the song into the dbs
def insertArtistSong(artists, song, songid, rep):
    artistids = []
    songRep = getSongRep(songid)
    if (songRep):
        insertSong(song, songid, rep + songRep)
    else:
        insertSong(song, songid, rep)
    for artist in artists:
        artistRep = getArtistRep(artist)
        artistids.append(insertArtist(artist, artistRep))
    for artistid in artistids:
        addArtistSongRelation(artistid, songid)

# EXAMPLE FUNCTION: This function shows how to add a user's songs to the db, when adding their songs you must also add
# a relation between the user and song
# given a username, song, and songid, insert the user and song into the db
def insertUserSong(username, song, songid):
    rep = getSongRep(songid)
    if not rep:
        insertSong(song, songid, BASEREP)
        rep = BASEREP
    userRep = getUserRep(username)
    if (userRep):
        newRep = userRep[0] + rep
        userid = insertUser(username, newRep, userRep[1])
    else:
        userid = insertUser(username, rep, BASEREP)
    addUserSongRelation(userid, songid)

# how to connect to the database and initalize variables, the cursor and connection are need for the functions to work,
# you need to figure out how to give each of the functions access to both the connection and the cursor
conn = sqlite3.connect('song.db')
conn.row_factory = make_dicts
c = conn.cursor()

# deletes all rows from all databases before every run
c.execute('DELETE FROM user')
c.execute('DELETE FROM artist')
c.execute('DELETE FROM song')
c.execute('DELETE FROM user_song')
c.execute('DELETE FROM artist_song')

# test cases

BASEREP = 5
firstSong = "Throw some mo"
firstArtists = ["Nikki Minaj", "Rae Sremmurd"]
firstUser = "wonnor"
secondSong = "No Type"
secondArtists = ["Rae Sremmurd"]
secondUser = "nhoran"

# Connor adds first song
insertArtistSong(firstArtists, firstSong, 1, 10)
insertUserSong(firstUser, firstSong, 1)

# Connor adds second song
insertArtistSong(secondArtists, secondSong, 2, 10)
insertUserSong(firstUser, secondSong, 2)

# Nate adds second song
insertArtistSong(secondArtists, secondSong, 2, 15)
insertUserSong(secondUser, secondSong, 2)

# Connor plays second song again
insertUserSong(firstUser, secondSong, 2)

print firstUser, "has a reputation of", getUserRep(firstUser), "and has added:", getUserSongs(firstUser)
print secondUser, "has a reputation of", getUserRep(secondUser), "and has added:", getUserSongs(secondUser)

print firstSong, "has a reputation of", getSongRep(1)
print secondSong, "has a reputation of", getSongRep(2)

print "Rae Sremmurd's songs:", getArtistSongs("Rae Sremmurd")
print "Nikki Minaj's songs:", getArtistSongs("Nikki Minaj")
