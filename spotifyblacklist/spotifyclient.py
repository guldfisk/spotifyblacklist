import dbus


def get_interface() -> dbus.Interface:
    return dbus.Interface(
        dbus.SessionBus().get_object('org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2'),
        dbus_interface = 'org.mpris.MediaPlayer2.Player',
    )
