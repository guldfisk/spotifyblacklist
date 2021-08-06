import typing as t

import dbus


def get_interface(bus: t.Optional[dbus.SessionBus] = None) -> dbus.Interface:
    return dbus.Interface(
        (bus or dbus.SessionBus()).get_object('org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2'),
        dbus_interface = 'org.mpris.MediaPlayer2.Player',
    )
