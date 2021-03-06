import librosa
import numpy as np

from system.AudioStream import AudioStream
from system.SignalProcessor import SignalProcessor
from system.SongPicker import SongPicker

SR = 44100
NEXT_SONG_PROCESSING_TIME = 5

class AudioController:
  def __init__(self):
    self._audio_stream_data = np.array([], dtype='float32').reshape(2,0)

    self._signal_processor = SignalProcessor()
    self._song_picker = SongPicker()
    self._new_song_processing_flag = False

    self._add_new_song()
    self._audio_stream = AudioStream(self._on_stream_callback)
    print('[AudioController] - On standby')

  def _on_stream_callback(self, frame_count):
    if (frame_count > self._audio_stream_data.size):
      print('[AudioController] - Stream data depleted.')

    time_remain = round(self._audio_stream_data.size/SR, 2)
    if time_remain < NEXT_SONG_PROCESSING_TIME:
      self._add_new_song()

    self._print_stream_status(frame_count)
    data = self._audio_stream_data[:, :frame_count]
    self._audio_stream_data = self._audio_stream_data[:, frame_count:]

    # convert two channel data to format accepted for pyaudio
    waved_data = np.vstack((data[0],data[1])).reshape((-1,),order='F')
    return waved_data

  def _add_new_song(self):
    if self._new_song_processing_flag: return
    self._new_song_processing_flag = True

    sig_action = self._signal_processor.interpret_signals()
    audio = self._song_picker.pick_song(sig_action)

    self._audio_stream_data = np.concatenate([self._audio_stream_data, audio], axis=1)

    self._new_song_processing_flag = False

  def on_signal_input(self, msg):
    if (msg.isdigit()):
      self._signal_processor.on_signal(msg)
    elif (msg == 's'):
      self.start_stream()
    elif (msg == 'p'):
      self.pause_stream()
    elif (msg == 'exit'):
      self.stop_stream()
    else:
      return

  def start_stream(self): self._audio_stream.start_stream()
  def pause_stream(self): self._audio_stream.pause_stream()

  def _print_stream_status(self, frame_count):
    secs = round(self._audio_stream_data.size/SR, 2)
    print('[AudioController] - Time remaining: {0}'.format(secs))
