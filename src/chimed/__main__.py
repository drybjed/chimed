# -*- coding: utf-8 -*-

# Copyright (C) 2022 Maciej Delmanowski <drybjed@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later


def main():
    print("Hello, chimed")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit('... aborted by user')
