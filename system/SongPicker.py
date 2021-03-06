import json
import random
import librosa
import numpy as np

from audio.Song import Song
from audio.Transition import Transition

from system.signal_action_constants import SIG_ACTIONS

SR = 44100
MIX_LEN = 32

name = 'full'
DATA_SET = './data/json/' + name + '.json'

class SongPicker:
  def __init__(self):
    self._all_songs = self._load_songs()
    self._cur_song = None

  def pick_song(self, sig_action):
    if not self._cur_song:
      # TODO: choose inital song from prexisting signals
      chosen_song = self._all_songs[128][0]
      raw_audio = self._retrieve_first_song_raw_audio(chosen_song)
    else:
      chosen_song = self._find_song_for_action(sig_action)
      raw_audio = self._retrieve_raw_audio(chosen_song)

    self._cur_song = chosen_song
    print('[SongPicker] - Picked:', chosen_song)
    return raw_audio

  def _load_songs(self):
    print('[SongPicker] - Loading Songs')
    bpm = {}
    with open(DATA_SET) as data_file:
      data = json.load(data_file)
    for song in data:
      bpm.setdefault(song['BPM'], [])
      new_song = Song(
        fname=song['File'],
        mix_in=song['MixIn'],
        mix_out=song['MixOut'],
        bpm=song['BPM'],
      )
      bpm[song['BPM']].append(new_song)
    return bpm

  def _find_song_for_action(self, sig_action):
    cur_bpm = self._cur_song.bpm
    all_bpms = sorted(self._all_songs.keys())

    if sig_action == SIG_ACTIONS['increase']:
      if cur_bpm == max(all_bpms):
        print('[SongPicker] - BPM at max:', cur_bpm)
      new_bpm_index = min(all_bpms.index(cur_bpm)+1, len(all_bpms)-1)
      new_bpm = all_bpms[new_bpm_index]
    elif sig_action == SIG_ACTIONS['decrease']:
      if cur_bpm == min(all_bpms):
        print('[SongPicker] - BPM at min:', cur_bpm)
      new_bpm_index = max(0, all_bpms.index(cur_bpm)-1)
      new_bpm = all_bpms[new_bpm_index]
    elif sig_action == SIG_ACTIONS['maintain']:
      new_bpm = cur_bpm

    # TODO: dont pick same songs
    song = random.choice(self._all_songs[new_bpm])
    return song

  # TODO: setup intro to song
  def _retrieve_first_song_raw_audio(self, song):
    trans_in = song.trans_in_audio()
    body = song.body_audio()
    raw_audio = np.concatenate([trans_in, body], axis=1)
    return raw_audio

  def _retrieve_raw_audio(self, song):
    out_song, in_song = self._cur_song, song
    transition = Transition(out_song, in_song, MIX_LEN)
    trans_audio = transition.merged_audio
    raw_audio = np.concatenate([trans_audio, in_song.body_audio()], axis=1)
    return raw_audio
