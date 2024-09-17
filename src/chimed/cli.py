# Copyright (C) 2023 Maciej Delmanowski <drybjed@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from .config import Configuration
from .daemon import Daemon
from .subcommands import Subcommands
import sys


class Interpreter(object):

    def __init__(self, args=None):
        self.args = args
        self.parsed_args = Subcommands(self.args)
        self.config = Configuration(args=self.parsed_args.args)

        if self.parsed_args.section == 'serve':
            self.do_serve(self.parsed_args.args)

        elif self.parsed_args.section == 'config':
            if self.parsed_args.command == 'list':
                self.do_config_list(self.parsed_args.args)
            elif self.parsed_args.command == 'get':
                self.do_config_get(self.parsed_args.args)

    def do_serve(self, args):
        daemon = Daemon(args=self.parsed_args.args, config=self.config)

    def do_config_get(self, args):
        if args.key:
            for option_name in args.key:
                self.config.config_get(option_name, format=args.format,
                                       keys=args.keys)
        else:
            self.config.config_get('.', format=args.format, keys=args.keys)

    def do_config_list(self, args):
        self.config.config_list()
