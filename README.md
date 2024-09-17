# chimed - wind chines in your UNIX environments

The `chimed` daemon is an equivalent of a wind chime in a Linux system. It
provides a way for other programs to create various sounds with simple
interfaces - interrupt signals, UDP or TCP packets, UNIX sockets.

## Installation

The `chimed` installation requires `libasound2` development files, needed to
build the `simpleaudio` Python module.

    sudo apt install libasound2-dev

You can install `chimed` from source in editable mode, if you want to work on it:

    git clone https://github.com/drybjed/chimed ~/src/github.com/drybjed/chimed
    pipx install --editable ~/src/github.com/drybjed/chimed

You can also install `chimed` from PyPI:

    pipx install chimed

## Usage

After installation, run the daemon in a terminal window:

    chimed serve

You can send commands to it using a FIFO file:

    # Play a bell sound
    echo "chime" >> $XDG_RUNTIME_DIR/chimed/fifo

The default installation includes a set of chimes and a corresponding
configuration for `vim` editor. You can check the `lib/vim/vimrc` file in the
repository to see an example configuration you need to include in your
`~/.vimrc` configuration to integrate with `chimed`. There's also an example
`systemd` unit file available, to run `chimed` as an user daemon.

The internal configuration can be viewed using:

    chimed config get

You can put YAML, TOML and JSON files in the `~/.config/chimed/conf.d/`
directory to add or modify configuration options. Currently there's not much
configuration to be done, a lot of things need to be implemented, so stay
tuned.

## Copyright

Copyright (C) 2022-2024 Maciej Delmanowski <drybjed@gmail.com>

## Attribution

This software includes sounds from [freesound.org](https://freesound.org/):

- ["richcraft chime 4"](https://freesound.org/people/richcraftstudios/sounds/454610/) by
  [richcraftstudios](https://freesound.org/people/richcraftstudios/), licensed
  under CCBY 3.0.

- ["Typewriter ding_near_mono"](https://freesound.org/people/_stubb/sounds/406243/) by
  [_stubb](https://freesound.org/people/_stubb/), licensed under CC0.

- ["Beep 03 Single"](https://freesound.org/people/PaulMorek/sounds/330050/) by
  [PaulMorek](https://freesound.org/people/PaulMorek/), licensed under CC0.

- ["Beep 04 Positive"](https://freesound.org/people/PaulMorek/sounds/330048/) by
  [PaulMorek](https://freesound.org/people/PaulMorek/), licensed under CC0.

- ["Click 02 Double"](https://freesound.org/people/PaulMorek/sounds/330076/) by
  [PaulMorek](https://freesound.org/people/PaulMorek/), licensed under CC0.

- ["Click 02 Single"](https://freesound.org/people/PaulMorek/sounds/330075/) by
  [PaulMorek](https://freesound.org/people/PaulMorek/), licensed under CC0.

- ["Swish 01"](https://freesound.org/people/PaulMorek/sounds/330066/) by
  [PaulMorek](https://freesound.org/people/PaulMorek/), licensed under CC0.

- ["e key"](https://freesound.org/people/uEffects/sounds/180998/) by
  [uEffects](https://freesound.org/people/uEffects/), licensed under CC0.

- ["l key"](https://freesound.org/people/uEffects/sounds/181003/) by
  [uEffects](https://freesound.org/people/uEffects/), licensed under CC0.

- ["s key"](https://freesound.org/people/uEffects/sounds/181002/) by
  [uEffects](https://freesound.org/people/uEffects/), licensed under CC0.
