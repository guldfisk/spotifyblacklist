from __future__ import annotations

import os
import typing as t

from spotifyblacklist import paths


class BlackList(object):

    def __init__(self, song_names: t.AbstractSet[str]):
        self._song_names = song_names

    @property
    def song_names(self) -> t.AbstractSet[str]:
        return self._song_names

    @classmethod
    def from_file(cls) -> BlackList:
        os.makedirs(paths.APP_DATA_PATH, exist_ok = True)
        try:
            with open(paths.LIST_PATH, 'r') as f:
                return cls(
                    {
                        ln
                        for ln in
                        (
                            ln.strip()
                            for ln in
                            f.readlines()
                        )
                        if ln and ln[0] != '#'
                    }
                )
        except FileNotFoundError:
            return cls(set())

    def __contains__(self, song: str) -> bool:
        return song in self._song_names

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._song_names})'
