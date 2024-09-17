# Copyright (C) 2023 Maciej Delmanowski <drybjed@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later


import simpleaudio
import soundfile
import pkgutil
import numpy
import os
import io


class Bell(object):

    def __init__(self, name, filename='', resource='', *args, **kwargs):

        self.name = name
        self.args = args
        self.kwargs = kwargs

        if resource:
            self.type = 'resource'
            try:
                self._resource_path = os.path.join('_data', 'audio', resource)

                # Load the wav file using pkgutil.get_data
                self._wav_data = pkgutil.get_data('chimed', self._resource_path)

                # Use soundfile to read the wav data
                self._audio_data, self._sample_rate = soundfile.read(
                        io.BytesIO(self._wav_data))

                # Convert audio_data to int16 (required by simpleaudio)
                self._audio_data = (self._audio_data * 32767).astype(numpy.int16)

                # Check the number of channels and convert to mono if necessary
                if len(self._audio_data.shape) > 1 and self._audio_data.shape[1] > 1:
                    self._audio_data = numpy.mean(self._audio_data, axis=1)

            except FileNotFoundError:
                print(f"Error: {self._resource_path} not found in package 'chimed'.")
                raise FileNotFoundError
            except Exception as e:
                print(f"Error: {e}")
                raise Exception

        elif filename:
            self.type = 'file'
            try:
                self._file_path = filename
                self._wav_data = simpleaudio.WaveObject.from_wave_file(self._file_path)
            except FileNotFoundError:
                print(f"Error: {self._resource_path} not found in package 'chimed'.")
                raise FileNotFoundError
            except Exception as e:
                print(f"Error: {e}")
                raise Exception

    def play(self):
        if self.type == 'resource':
            try:
                self._play_obj = simpleaudio.play_buffer(self._audio_data, num_channels=1,
                                                         bytes_per_sample=2,
                                                         sample_rate=self._sample_rate)
                if self.kwargs.get('wait', False):
                    self._play_obj.wait_done()
            except Exception:  # Better exception?
                # Catch "Too many open files" error and handle it gracefully
                # This happens when chimes are played too rapidly for the
                # system to handle
                # FIXME: "ALSA lib pcm.c:8570:(snd_pcm_recover) underrun occurred"
                # This still spams the stderr, not sure how to avoid it from inside
                # Python.
                pass
        elif self.type == 'file':
            self._play_obj = self._wav_data.play()
            if self.kwargs.get('wait', False):
                self._play_obj.wait_done()
