# Copyright (C) 2022-2023 Maciej Delmanowski <drybjed@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later


import chimed
import atexit
import shutil
import sys
import xdg
import os


comm_fifo = os.path.join(xdg.xdg_runtime_dir(), 'chimed', 'fifo')


def cleanup():
    shutil.rmtree(os.path.dirname(comm_fifo))


def main():

    os.mkdir(os.path.dirname(comm_fifo))
    os.mkfifo(comm_fifo)

    chime = chimed.Bell('chime1', resource='richcraft-chime-4.wav')

    while True:
        with open(comm_fifo, 'r') as fifo:
            for line in fifo:
                chime.play()
    args = sys.argv
    interpreter = chimed.Interpreter(args)

atexit.register(cleanup)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit('... aborted by user')
