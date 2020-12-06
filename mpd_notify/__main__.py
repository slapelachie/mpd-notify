import argparse
import sys
import time
import os

from .mpd import MPD
from .notify import Notify


def get_args():
    arg = argparse.ArgumentParser(
        description="MPD notification handler",
        usage="mpd-notify [options]",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    arg.add_argument("--host", default="localhost", help="Location of the mpd host")
    arg.add_argument(
        "--port", default=6600, type=int, help="The port which mpd is running"
    )
    arg.add_argument("--id", default=660, type=int, help="What the notification id is")
    arg.add_argument(
        "--music-dir", default="~/Music", help="The directory which mpd is playing from"
    )
    arg.add_argument(
        "--watch",
        action="store_true",
        help="Continously show notifications on song change",
    )
    arg.add_argument("--fork", action="store_true", help="Fork process to background")

    return arg


def parse_args(parser):
    args = parser.parse_args()

    mpd_host = args.host if args.host else "localhost"
    mpd_port = args.port if args.port else 6600
    music_dir = args.music_dir if args.music_dir else "~/Music"
    notify_id = args.id if args.id else 660

    try:
        MPDClient = MPD(mpd_host, mpd_port, music_dir)
    except ConnectionRefusedError:
        print("Could not connect to mpd, exiting...")
        exit(1)

    NotifManager = Notify(notification_id=notify_id)

    if args.watch:
        try:
            if args.fork:
                pid = os.fork()
                if pid > 0:
                    print("Forked to {}".format(pid))
                    sys.exit(0)

            log = [None, None]
            while True:
                log.append(MPDClient.get_state())

                if log[-1] == "stop":
                    time.sleep(1)
                    continue

                if log[-1] != "stop" and log[-2] == "stop":
                    MPDClient.update()

                if MPDClient.get_title() == None:
                    NotifManager.notify(MPDClient.get_fullfile(), "")
                else:
                    NotifManager.notify(
                        MPDClient.get_title(),
                        "{} - {}".format(MPDClient.get_artist(), MPDClient.get_album()),
                        icon=MPDClient.get_cover(),
                    )

                MPDClient.watch()
        except KeyboardInterrupt:
            sys.exit(0)
    else:
        if MPDClient.get_state() == "stop":
            print("Nothing playing...")
            sys.exit(0)

        if MPDClient.get_title() == None:
            NotifManager.notify(MPDClient.get_fullfile(), "")
        else:
            NotifManager.notify(
                MPDClient.get_title(),
                "{} - {}".format(MPDClient.get_artist(), MPDClient.get_album()),
                icon=MPDClient.get_cover(),
            )


def main():
    parser = get_args()
    parse_args(parser)


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