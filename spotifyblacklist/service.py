import os
import time

import dbus
from dbus.mainloop.glib import DBusGMainLoop

from gi.repository import GLib

from spotifyblacklist import paths
from spotifyblacklist.blacklist import BlackList


class SkipperService(object):

    def __init__(self):
        self._black_list = None

        self._dbus_loop = DBusGMainLoop()

        self._session_bus = dbus.SessionBus(mainloop = self._dbus_loop)
        self._proxy = self._session_bus.get_object('org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')
        self._spotify_interface = dbus.Interface(self._proxy, dbus_interface = 'org.mpris.MediaPlayer2.Player')

        self._lt = 0
        self._last_skip = ''

        self._list_modified_last = 0

    def reload_black_list(self) -> None:
        self._black_list = BlackList.from_file().from_file()

    def check_black_list(self) -> bool:
        last_modified = os.stat(paths.LIST_PATH).st_mtime
        if last_modified != self._list_modified_last:
            self.reload_black_list()
            self._list_modified_last = last_modified
        return True

    def _signal_handler(self, *args, **kwargs) -> None:
        if args and args[0] == 'org.mpris.MediaPlayer2.Player':
            if args[1].get('PlaybackStatus') == 'Playing':
                song_title = args[1]['Metadata']['xesam:title']
                if (
                    song_title in self._black_list
                    and (
                        time.time() > self._lt + 2
                        or self._last_skip != song_title
                    )
                ):
                    self._spotify_interface.Next()
                    self._lt = time.time()
                    self._last_skip = song_title

    def run(self) -> None:
        self.check_black_list()

        self._session_bus.add_signal_receiver(self._signal_handler)

        GLib.timeout_add_seconds(5, self.check_black_list)
        GLib.MainLoop().run()


def run():
    SkipperService().run()


if __name__ == '__main__':
    run()
