import datetime

import click
import dbus

from spotifyblacklist import paths
from spotifyblacklist.blacklist import BlackList
from spotifyblacklist.spotifyclient import get_interface


class AliasedGroup(click.Group):

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [
            x
            for x in
            self.list_commands(ctx)
            if x.startswith(cmd_name)
        ]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: {}'.format(', '.join(sorted(matches))))


@click.group(cls = AliasedGroup)
def main() -> None:
    """
    Manage spotify blacklist.
    """
    pass


@main.command(name = 'list')
def list_blacklist() -> None:
    """
    List blacklisted songs.
    """
    for song_name in sorted(BlackList.from_file().song_names):
        print(song_name)


@main.command(name = 'add')
@click.option('--stay', default = False, type = bool, is_flag = True, show_default = True, help = 'Don\'t skip.')
def add(stay: bool) -> None:
    """
    Add current song to blacklist.
    """
    with open(paths.LIST_PATH, 'a') as f:
        f.write('\n')
        f.write(f'# added {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n')
        f.write(
            dbus.Interface(
                dbus.SessionBus().get_object('org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2'),
                'org.freedesktop.DBus.Properties',
            ).Get('org.mpris.MediaPlayer2.Player', 'Metadata')['xesam:title'] + '\n'
        )
    if not stay:
        get_interface().Next()


@main.command(name = 'next')
def next_song() -> None:
    """
    Next song.
    """
    get_interface().Next()


@main.command(name = 'previous')
def previous_song() -> None:
    """
    Previous song.
    """
    get_interface().Previous()


@main.command(name = 'playpause')
def previous_song() -> None:
    """
    Play / Pause.
    """
    get_interface().PlayPause()


@main.command(name = 'up')
@click.option('--amount', '-a', default = 10, type = int, help = 'Percentage point value increase', show_default = True)
def volume_up(amount: int) -> None:
    """
    Adjust volume up.
    """
    from volume import adjust_volume
    adjust_volume(amount)


@main.command(name = 'down')
@click.option('--amount', '-a', default = 10, type = int, help = 'Percentage point value decrease', show_default = True)
def volume_down(amount: int) -> None:
    """
    Adjust volume down.
    """
    from volume import adjust_volume
    adjust_volume(-amount)


if __name__ == '__main__':
    main()
