# Copyright (C) 2023 Maciej Delmanowski <drybjed@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from .bell import Bell
import atexit
import errno
import shutil
import sys
import xdg
import os


class Daemon(object):

    def __init__(self, args=None, config=None):

        self._args = args
        self._config = config
        self._fifo_bell = os.path.join(xdg.BaseDirectory.get_runtime_dir(), 'chimed', 'fifo')
        self._fifo_dir = os.path.dirname(self._fifo_bell)

        try:
            os.mkdir(self._fifo_dir)
        except FileExistsError:
            if os.path.exists(self._fifo_bell):
                try:
                    fd = os.open(self._fifo_bell, os.O_WRONLY | os.O_NONBLOCK)
                    os.close(fd)
                except OSError as exc:
                    if exc.errno == errno.ENXIO:
                        shutil.rmtree(self._fifo_dir)
                        os.mkdir(self._fifo_dir)
                    else:
                        raise
                else:
                    print('Another copy of chimed is running already. Exiting.')
                    sys.exit(1)
            else:
                shutil.rmtree(self._fifo_dir)
                os.mkdir(self._fifo_dir)

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
        shutil.rmtree(self._fifo_dir)
