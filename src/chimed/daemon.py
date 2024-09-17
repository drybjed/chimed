# Copyright (C) 2023 Maciej Delmanowski <drybjed@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from .bell import Bell
import atexit
import shutil
import sys
import xdg
import os


class Daemon(object):

    def __init__(self, args=None, config=None):

        self._args = args
        self._config = config
        self._fifo_bell = os.path.join(xdg.xdg_runtime_dir(), 'chimed', 'fifo')

        os.mkdir(os.path.dirname(self._fifo_bell))
        os.mkfifo(self._fifo_bell)

        atexit.register(self.cleanup)

        self.chime = Bell('chime1', resource='richcraft-chime-4.wav')

        while True:
            with open(self._fifo_bell, 'r') as fifo:
                for line in fifo:
                    self.chime.play()

    def cleanup(self):
        shutil.rmtree(os.path.dirname(self._fifo_bell))