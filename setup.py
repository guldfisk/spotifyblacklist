import os

from setuptools import setup


def package_files(directory):
    paths = []
    for path, directories, file_names in os.walk(directory):
        for filename in file_names:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files('spotifyblacklist')

setup(
    name = 'spotifyblacklist',
    version = '1.0',
    packages = ['spotifyblacklist'],
    package_data = {'': extra_files},
    include_package_data = True,
    install_requires = [
        'appdirs',
        'dbus-python',
        'pgi',
        'click',
    ],
)
