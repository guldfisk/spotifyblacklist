import subprocess
import re
import typing as t


def get_current_volume() -> t.Tuple[int, int]:
    s = subprocess.check_output(['pactl', 'list', 'sink-inputs']).decode('utf')
    for ss in s.split('Sink Input'):
        if 'spotify-client' in ss:
            idx = re.search('#(\d+)', ss)
            vol = re.search('Volume.*?(\d+)%', ss)
            return int(idx.group(1)), int(vol.group(1))
    raise RuntimeError('spotify not found')


def set_volume(idx: int, value: int) -> None:
    subprocess.call(('pactl', 'set-sink-input-volume', str(idx), str(value) + '%'))


def adjust_volume(delta: int) -> int:
    idx, volume = get_current_volume()
    new_volume = max(min(volume + delta, 100), 0)
    set_volume(idx, new_volume)
    return new_volume
