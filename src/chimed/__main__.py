# Copyright (C) 2022-2023 Maciej Delmanowski <drybjed@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later


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

atexit.register(cleanup)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit('... aborted by user')
