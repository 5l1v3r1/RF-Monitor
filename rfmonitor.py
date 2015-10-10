#! /usr/bin/env python
#
#
# RF Monitor
#
#
# Copyright 2015 Al Brown
#
# RF signal monitor
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import argparse
import os
import sys

import wx

from rfmonitor.cli import Cli
from rfmonitor.constants import APP_NAME
from rfmonitor.gui import RfMonitor, FrameMain


def __arguments():
    parser = argparse.ArgumentParser(prog="rfmonitor.py",
                                     description='RF signal monitor')

    parser.add_argument('-c', help='Command line mode', action='store_true')
    parser.add_argument("file", nargs='?')
    args = parser.parse_args()

    if args.c and args.file is None:
        sys.stderr.write('Filename required in command line mode')
        exit(1)

    if args.file is not None and not os.path.exists(args.file):
        sys.stderr.write('File not found')
        exit(1)

    return args


if __name__ == '__main__':
    print APP_NAME + "\n"

    args = __arguments()

    if args.c:
        cli = Cli(args.file)
    else:
        app = RfMonitor()
        app.SetClassName(APP_NAME)
        wx.Locale().Init2()
        frame = FrameMain()
        if args.file is not None:
            frame.open(args.file)

        app.MainLoop()
