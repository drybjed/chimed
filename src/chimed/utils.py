# Copyright (C) 2022 David Härdeman <david@hardeman.nu>
# SPDX-License-Identifier: GPL-3.0-or-later

import os


def unexpanduser(path):
    """Replace the absolute path of the home directory with '~'

    This function will replace the full path of the home directory with the '~'
    shorthand, but only if it is present at the start of the absolute path.
    This workaround is needed in cases where home directory string can be
    encountered inside of the path, for example if home directory is symlinked
    from a different place in the filesystem."""
    if path.startswith(os.path.expanduser('~')):
        return path.replace(os.path.expanduser('~'), '~', 1)
    else:
        return path
