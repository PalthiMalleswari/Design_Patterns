# Reference - https://algomaster.io/learn/lld/iterator

"""
It provides a strandard way to access elements of a collection sequentially without
exposing its internal structure

Need:

1.  you need to traverse a collection(list,tree,graph) in a consistent and flexible
    way
2.  you want to support multiple ways to iterate(forward,reverse,shuffle)
3.  you want to decouple the traversin logic from collection structure(so client
    shouldn't depend on internal repr)

"""

# ========= Problem =========
# we've a music streaming app, users can create playlist,add songs
# play them in various ways (one by one)

class Playlist:

    def __init__(self):
        
        self.songs = []

    def add_song(self,sng):

        self.songs.append(sng)

    def get_songs(self):
        
        return self.songs

class MusicPlayer:

    def play_all(self,playlist:Playlist):

        for song in playlist.get_songs():

            print(f"Playing Song.. %% {song}..")

ply = Playlist()

ply.add_song("Jelsa, My Heart is Beating..")
ply.add_song("Three, Na kallallo kala nuv anta..")
ply.add_song("Shape of U, i'm in Love with the shape you")

MusicPlayer().play_all(ply)

# What's wrong with this Design ??

"""
1. No Encapsulation : Client (Music Player) can add un autherized songs,remove sorgs
    clear the playlist playlist.get_songs().clear()
2. Tightly couples client to implementation : let's say playlist changes it's datastructure to 
    LinkedList<Songs> or songs should be fetch from DB lazily instead of fetching all at once
3. Limited Traversal Options : user want to play their songs in reverse or shuffle or skip disliked
    songs, it need a seperate loop logic in client, playlist has no controll over its contents
4. Difficult Testing : Player can't be tested easily, we need to mock playlist's behaviour
"""

# =========== Iterator Pattern ============

"""
It defines a seperate object, the iterator, that encapsilates the details of traversing a collection
instead of exposing its internal structure, the collection provides an iterator that client
use to access elements sequentially

it seperates two concerns
1. collector knows how to store elements
2. Iterator knows how to traverse those elements

Key Components
1. Iterator Interface (Declares operations required to traverse a collection)
2. Concrete Iterators (Implements the Iterator for Specific collection)
3. IterableCollection : Declares a method for creating an iterator
4. ConcreteCollection : stores elements a returns an iterator when needed

Iterator Object is helpful in multi threaded applications, to simulate multiple
traversals at a time independently
"""

# =============== Implementation ==============

from abc import ABC,abstractmethod

# Interfaces

class Iterator(ABC):

    @abstractmethod
    def has_next(self):
        pass

    @abstractmethod
    def next(self):
        pass

class IterableCollection(ABC):

    @abstractmethod
    def create_iterator(self):
        pass

    @abstractmethod
    def create_reverse_iterator(self):
        pass

# Concrete Collection

class Playlist(IterableCollection):

    def __init__(self):    
        self.songs = []
    
    def add_song(self,song):
        self.songs.append(song)
    
    def get_song_at(self,ind):
        return self.songs[ind]
    
    def get_size(self):
        return len(self.songs)
    
    def create_iterator(self):
        return PlaylistIterator(self)
    
    def create_reverse_iterator(self):
        return PlaylistReversalIterator(self)

# Concrete Iterator 1

class PlaylistIterator(Iterator):

    def __init__(self,playlist:Playlist):
        self.playlist =  playlist
        self.index = 0
    
    def has_next(self):
        return self.playlist.get_size()>self.index
    
    def next(self):
        
        song = self.playlist.get_song_at(self.index)
        self.index += 1
        return song
    
# Concrete Iterator 2

class PlaylistReversalIterator(Iterator):

    def __init__(self,playlist:Playlist):
        self.playlist =  playlist
        self.index = playlist.get_size()-1
    
    def has_next(self):
        return self.index>=0 and self.playlist.get_size()>self.index
    
    def next(self):
        
        song = self.playlist.get_song_at(self.index)
        self.index -= 1
        return song
    
def music_player_demo():

    pl_list = Playlist()

    pl_list.add_song("Shape of you..")
    pl_list.add_song("Blinding Light")
    pl_list.add_song("We don't Talk Anymore")

    iterator = pl_list.create_iterator()
    rev_iterator = pl_list.create_reverse_iterator()
    
    print("Playing Playlist")

    while iterator.has_next():

        print(f" Playing % {iterator.next()} ")

    print("Playing Playlist In Reverse")

    while rev_iterator.has_next():

        print(f" Playing % {rev_iterator.next()} ")

music_player_demo()