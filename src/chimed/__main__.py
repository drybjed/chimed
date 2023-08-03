# Copyright (C) 2022-2023 Maciej Delmanowski <drybjed@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later


import chimed
import sys


def main():

    args = sys.argv
    interpreter = chimed.Interpreter(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit('... aborted by user')
