from .mpd import MPD
from .notify import Notify


def main():
    MPDClient = MPD("~/Music")
    NotifManager = Notify()
    while True:
        NotifManager.notify(
            MPDClient.get_title(),
            "{} - {}".format(MPDClient.get_artist(), MPDClient.get_album()),
            icon=MPDClient.get_cover(),
        )
        MPDClient.watch()


if __name__ == "__main__":
    main()

"""
mpd-notify - Notification wrapper for mpd
Copyright (C) 2020  slapelachie

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Find the full license in the root of this project
"""