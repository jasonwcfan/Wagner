import json
from data_setup import load_songs
from mashability import mash_pairs
from mix_songs import blend_song

from pprint import pprint

def main():
	songs = load_songs()
	pair_mashability = mash_pairs(songs)
	mix_list = generate_mix(songs, pair_mashability)
	pprint(pair_mashability)

if __name__ == '__main__':
	main()
