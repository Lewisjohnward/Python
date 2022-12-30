# A simple program that plays MP3 given as arg

# Import vlc from python-vlc module
import vlc
# Time to sleep program whilst playing
import time
# Sys for command line arguments
import sys

def Sound(sound):
    vlc_instance = vlc.Instance()
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(sound)
    player.set_media(media)
    player.play()
    time.sleep(1.5)
    duration = player.get_length() / 1000
    time.sleep(duration)

# Play audio from file given as command line arg
Sound(sys.argv[1])

