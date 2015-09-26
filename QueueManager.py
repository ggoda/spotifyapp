import Constants
import DBConvenience

class QueueManager:

    class QueueElement:
        def __init__(self, song, songID, artist, user, initialweight):
            self.song = song
            self.songID = songID
            self.artist = artist
            self.user = user
            self.initialweight = initialweight
            self.varweight = initialweight

        def songElapsed(self):
            self.varweight *= SONG_ELAPSED_MULT
            return self

    def __init__(self):
        self.queue = []

    def enQ(self, song, songID, artist, user):
        songRep = getSongRep(songID)
        artistRep = getArtistRep(artist)
        userRep = getUserRep(username)
        
        weight = (songRep * INITIALWEIGHT_SONG_PROP + \
                  artistRep * INITIALWEIGHT_ARTIST_PROP + \
                  userRep * INITIALWEIGHT_USER_PROP) / \
                  INITIALWEIGHT_TOTAL_PROP
        elem = QueueElement(song, artist, user, weight)
        self.queue.append(elem)

    def deQ(self):
        self.queue.sort(key = lambda elem: elem.varweight)
        elem = self.queue.pop()
        ## increase weight of all other songs
        self.queue = list(map(lambda elem: elem.songElapsed, queue))
        return elem

    def bump(
        
        
