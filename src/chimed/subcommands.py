# Copyright (C) 2023 Maciej Delmanowski <drybjed@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import os
import sys

# Detect the chimed version from the Python module. If the version is not
# available, we are in a development environment in which case we use a stub
# version number to avoid errors.
try:
    from .__version__ import __version__
except ModuleNotFoundError:
    __version__ = "0.0.0"


class Subcommands(object):

    def __init__(self, args=None):
        self.args = args

        self.global_parser = argparse.ArgumentParser(add_help=False)
        self.global_parser.add_argument('--no-defaults', action="store_true",
                                             help='do not load configuration defaults ')
        self.global_parser.add_argument('-v', '--verbose', action="count",
                                        help='increase output verbosity '
                                             '(e.g., -vv is more than -v)')

        parser = argparse.ArgumentParser(
                description="chimed - add bells and whistles to your environment",
                usage='''chimed <section> [<args>]

Sections:
    serve    start chimed daemon
    config   display chimed configuration options''')

        parser.add_argument('section', help='Section to run')
        parser.add_argument('--version', action='version',
                            version='%(prog)s {version}'
                                    .format(version=__version__))

        self._section = parser.parse_args(self.args[1:2])
        self.section = self._section.section
        if not hasattr(self, 'do_' + self._section.section):
            print('Error: unrecognized section:', self._section.section)
            parser.print_help()
            sys.exit(1)
        getattr(self, 'do_' + self._section.section)()

    def add_bool_argument(self, parser, name, default=False,
                          required=False, help=None, no_help=None):
        group = parser.add_mutually_exclusive_group(
                required=required)
        group.add_argument('--' + name, dest=name,
                           help=help, action='store_true')
        group.add_argument('--no-' + name, dest=name,
                           help=no_help, action='store_false')
        parser.set_defaults(**{name: default})

    def do_serve(self):
        parser = argparse.ArgumentParser(
                parents=[self.global_parser],
                usage='chimed serve [<args>]',
                description='run chimed daemon')
        self.args = parser.parse_args(self.args[2:])

    def do_config(self):
        parser = argparse.ArgumentParser(
                description='manage chimed configuration state',
                usage='''chimed config <command> [<args>]

Commands:
    get     return value of a specific configuration option
    list    list configuration files parsed by chimed''')
        parser.add_argument('command', help='config command to run')
        self._command = parser.parse_args(self.args[2:3])
        self.command = self._command.command
        if not hasattr(self, 'do_config_' + self._command.command):
            print('Error: unrecognized command:', self._command.command)
            parser.print_help()
            sys.exit(1)
        getattr(self, 'do_config_' + self._command.command)()

    def do_config_list(self):
        parser = argparse.ArgumentParser(
                usage='chimed config list [<args>]',
                description='list configuration files parsed by chimed')
        parser.add_argument('-v', '--verbose', action="count",
                            help='increase output verbosity '
                                 '(e.g., -vv is more than -v)')
        self.args = parser.parse_args(self.args[3:])

    def do_config_get(self):
        parser = argparse.ArgumentParser(
                parents=[self.global_parser],
                usage='chimed config get [<args>] [--] <key>',
                description='return value of specific chimed option')
        parser.add_argument('--format', type=str, nargs='?',
                            choices=['json', 'toml', 'unix', 'yaml'],
                            default='unix',
                            help='output format (default: %(default)s)')
        parser.add_argument('-k', '--keys', default=False,
                            help='list configuration keys '
                                 'at the specified level',
                            action='store_true')
        parser.add_argument('key', type=str,
                            nargs=argparse.REMAINDER,
                            help='name of the '
                                 'configuration option')
        self.args = parser.parse_args(self.args[3:])
