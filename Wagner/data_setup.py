import json
from objects.Song import Song

name = 'TwoSongs'
DATA_SET = './data/json/' + name + '.json'

def load_songs():
	with open(DATA_SET) as data_file:
		data = json.load(data_file)

	songs = []
	for song in data:
		new_song = Song(
			name=song['Name'],
			fname=song['File'],
			mix_in=song['MixIn'],
			mix_out=song['MixOut'],
			unary_factor=song['Unary'],
			song_id=song['SongId'],
			bpm=song['BPM'],
			key=song['Key']
		)
		songs.append(new_song)

	return songs
