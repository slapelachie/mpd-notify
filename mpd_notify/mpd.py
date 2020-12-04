import mutagen
import os
import io
import base64
import time
from PIL import Image

from mpd import MPDClient


class MPD:
    def __init__(self, host, port, music_dir):
        self.host = host
        self.port = port
        self.music_dir = music_dir

        self.mpd = MPDClient()
        self.mpd.connect(self.host, self.port)

        self.title = self.get_title()
        self.artist = self.get_artist()
        self.album = self.get_album()
        self.file = self.get_file()

    def get_state(self):
        return self.mpd.status()["state"]

    def get_artist(self):
        return self.mpd.currentsong().get("artist")

    def get_album(self):
        return self.mpd.currentsong().get("album")

    def get_cover(self):
        file_path = os.path.expanduser(os.path.join(self.music_dir, self.file))
        mf = mutagen.File(file_path)
        pictureData = None
        out_path = "/tmp/mpd-notify.png"

        try:
            if isinstance(mf.tags, mutagen._vorbis.VComment) or isinstance(
                mf, mutagen.ogg.OggFileType
            ):
                artwork_bytes = base64.b64decode(mf["metadata_block_picture"][0])
                picture = mutagen.flac.Picture(artwork_bytes)
                pictureData = io.BytesIO(picture.data)

            elif isinstance(mf.tags, mutagen.id3.ID3) or isinstance(
                mf, mutagen.id3.ID3FileType
            ):
                artwork_bytes = mf.tags["APIC:"].data
                pictureData = io.BytesIO(artwork_bytes)

            img = Image.open(pictureData)
            img = img.resize((96, 96))
            img.save(out_path)
            return out_path
        except:
            return None

    def get_file(self):
        return self.mpd.currentsong().get("file")

    def get_title(self):
        return self.mpd.currentsong().get("title")

    def update(self):
        self.title = self.get_title()
        self.album = self.get_album()
        self.artist = self.get_artist()
        self.file = self.get_file()
        self.cover = self.get_cover()

    def watch(self):
        old_file = self.file
        while True:
            # Wait until mpd status change
            self.mpd.idle()
            if self.get_state() == "stop":
                break

            self.update()

            # prevent multiple undesired notification
            if old_file != self.file:
                time.sleep(1)
                break


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