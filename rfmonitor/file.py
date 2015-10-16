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

from collections import OrderedDict
import json

from rfmonitor.constants import APP_NAME
from rfmonitor.signals import Signal


VERSION = 1


def save_recordings(filename, settings):

    jsonMonitors = []
    for monitor in settings.get_monitors():
        jsonMonitor = OrderedDict()
        jsonMonitor['Enabled'] = monitor.enabled
        jsonMonitor['Frequency'] = int(monitor.freq * 1e6)
        jsonMonitor['Threshold'] = monitor.threshold
        jsonMonitor['Signals'] = [signal.to_list()
                                  for signal in monitor.signals]
        jsonMonitors.append(jsonMonitor)

    fileData = OrderedDict()
    fileData['Version'] = VERSION
    fileData['Frequency'] = settings.get_freq() * 1e6
    fileData['Monitors'] = jsonMonitors

    data = [APP_NAME, fileData]

    handle = open(filename, 'wb')
    handle.write(json.dumps(data, indent=4))
    handle.close()


def load_recordings(filename, settings):
    handle = open(filename, 'rb')
    data = json.loads(handle.read())
    handle.close()

    _header = data[0]
    _version = data[1]['Version']
    settings.freq = data[1]['Frequency'] / 1e6
    monitors = data[1]['Monitors']

    settings.clear_monitors()
    for monitor in monitors:
        signals = [Signal().from_list(signal) for signal in monitor['Signals']]
        settings.add_monitor(monitor['Enabled'],
                             monitor['Frequency'] / 1e6,
                             monitor['Threshold'],
                             signals)


def format_recording(freq, recording):
    record = OrderedDict()
    record['Start'] = recording.start
    record['End'] = recording.end
    record['Level'] = recording.level
    if recording.location is not None:
        record['location'] = recording.location

    signal = OrderedDict()
    signal['Frequency'] = int(freq * 1e6)
    signal['Signal'] = record

    return json.dumps(signal)


if __name__ == '__main__':
    exit(1)
    print 'Please run rfmonitor.py'
