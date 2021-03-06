import json
from audio.Mix import Mix
from audio.Song import Song
from audio.Mashability import Mashability
from pprint import pprint

name = 'full'
DATA_SET = './data/json/' + name + '.json'

def load_songs():
	with open(DATA_SET) as data_file:
		data = json.load(data_file)

	songs = []
	for song in data:
		new_song = Song(
			fname=song['File'],
			mix_in=song['MixIn'],
			mix_out=song['MixOut'],
			bpm=song['BPM'],
		)
		songs.append(new_song)
	return songs

def main():
	songs = load_songs()
	mash_seq = Mashability(songs).seq
	mix = Mix(songs)

if __name__ == '__main__':
	main()
