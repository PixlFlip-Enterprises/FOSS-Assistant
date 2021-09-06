import os
import random
from pydub import AudioSegment
from pydub.playback import play
from tinytag import TinyTag

currentDirectory = os.getcwd()



# plays single song
def playsong(directory):
    song = AudioSegment.from_mp3(currentDirectory + directory)
    play(song)


# voice
def playVoice(directory):
    song = AudioSegment.from_wav(currentDirectory + directory)
    play(song)


# gets tagged information of music file
def gettag(file):
    audio = TinyTag.get(file)
    return [audio.title, audio.artist, audio.genre]

    # EXTRA CODE SO I DONT HAVE TO LOOK IT UP LATER
    # print("Year Released: " + audio.year)
    # print("Bitrate:" + str(audio.bitrate) + " kBits/s")
    # print("Composer: " + audio.composer)
    # print("Filesize: " + str(audio.filesize) + " bytes")
    # print("AlbumArtist: " + audio.albumartist)
    # print("Duration: " + str(audio.duration) + " seconds")
    # print("TrackTotal: " + str(audio.track_total))


# queues music by artist
def queuebyartist(artist):
    path = currentDirectory + "/Music"
    list_of_files = []

    # array for matching songs
    lst = []

    for root, dirs, files in os.walk(path):
        for file in files:
            list_of_files.append(os.path.join(root, file))
    for name in list_of_files:
        # get audio file artist
        audio = TinyTag.get(name)
        # compare and if match
        if artist == audio.artist:
            lst.append(name)
        return lst


# queues music by album
def queuebyalbum(album):
    path = currentDirectory + "/Music"
    list_of_files = []

    # array for matching songs
    lst = []

    for root, dirs, files in os.walk(path):
        for file in files:
            list_of_files.append(os.path.join(root, file))
    for name in list_of_files:
        # get audio file artist
        audio = TinyTag.get(name)
        # compare and if match
        if album == audio.artist:
            lst.append(name)
        return lst


# queues everything
def queueAll(directory):
    dir = directory.__str__().replace("\n", "")
    path = dir
    list_of_files = []

    # array for matching songs
    lst = []

    for root, dirs, files in os.walk(path):
        for file in files:
            list_of_files.append(os.path.join(root, file))
    for name in list_of_files:
        lst.append(name)

    return lst


# rewrite this
def playQueue(queue):
    for song in queue:
        songTitle = AudioSegment.from_mp3(song)
        play(songTitle)


# shuffles the array
def shuffleQueue(queue):
    random.shuffle(queue)
    return queue
