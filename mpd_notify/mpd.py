"""
Original version taken from
https://raw.githubusercontent.com/chuugar/mpdnotify/master/mpdnotify/notify.py
"""

import pathlib
import mutagen
import os
import io
import base64
from PIL import Image

from subprocess import run
from mpd import MPDClient


class MPD:
    def __init__(self, music_dir, host="localhost", port=6600, appname="mpd"):
        self.host = host
        self.port = port
        self.appname = appname
        self.music_dir = music_dir

        self.mpd = MPDClient()
        self.mpd.connect(self.host, self.port)

        self.title = self.get_title()
        self.artist = self.get_artist()
        self.album = self.get_album()
        self.file = self.get_file()

        self.body, self.notify_run = "", ""
        self.garbagecover = []

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

    def watch(self):
        old_file = self.file
        while True:
            # Wait until change
            self.mpd.idle()

            self.title = self.get_title()
            self.album = self.get_album()
            self.artist = self.get_artist()
            self.file = self.get_file()
            self.cover = self.get_cover()

            # prevent multiple undesired notification
            if old_file != self.file:
                break
