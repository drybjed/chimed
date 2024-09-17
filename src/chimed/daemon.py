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
        self._fifo_bell = os.path.join(xdg.BaseDirectory.get_runtime_dir(), 'chimed', 'fifo')

        try:
            os.mkdir(os.path.dirname(self._fifo_bell))
        except FileExistsError:
            print('Another copy of chimed is running already. Exiting.')
            sys.exit(1)

        os.mkfifo(self._fifo_bell)

        atexit.register(self.cleanup)

        self.bells = {}

        for key, value in self._config.get('bells').items():
            self.bells[key] = Bell(key, resource=value['resource'])

        while True:
            try:
                with open(self._fifo_bell, 'r') as fifo:
                    for line in fifo:
                        line = line.strip()
                        for element in self._config.get('inputs'):
                            if line == element['string']:
                                self.bells[element['output']].play()
            except KeyboardInterrupt:
                sys.exit()

    def cleanup(self):
        shutil.rmtree(os.path.dirname(self._fifo_bell))
