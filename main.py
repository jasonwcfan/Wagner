import json
from data_setup import load_songs

from objects.Playlist import Playlist

from pprint import pprint

def main():
	songs = load_songs()
	playlist = Playlist(songs)

	# mix.write_mix()

if __name__ == '__main__':
	main()
