import subprocess
import time

import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

from spotifyblacklist.blacklist import BlackList


class SkipperService(object):

    def __init__(self, black_list: BlackList):
        self._black_list = black_list

        self._dbus_loop = DBusGMainLoop()
        self._session_bus = dbus.SessionBus(mainloop = self._dbus_loop)

        self._bus_data = ("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")
        self._spotify_bus = self._session_bus.get_object(*self._bus_data)

        self._interface = dbus.Interface(self._spotify_bus, "org.freedesktop.DBus.Properties")

        self._metadata = self._interface.Get("org.mpris.MediaPlayer2.Player", "Metadata")

        self._lt = 0

    def _signal_handler(self, *args, **kwargs) -> None:
        if args and args[0] == 'org.mpris.MediaPlayer2.Player':
            if args[1]['PlaybackStatus'] == 'Playing' and args[1]['Metadata']['xesam:title'] in self._black_list:
                if time.time() > self._lt + 2:
                    subprocess.run(
                        'dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next',
                        shell = True,
                    )
                    self._lt = time.time()

    def run(self) -> None:
        self._session_bus.add_signal_receiver(self._signal_handler)

        loop = GLib.MainLoop()
        loop.run()


def run():
    SkipperService(BlackList.from_file()).run()


if __name__ == '__main__':
    run()
