# mpd-notify

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/L3L726D8I)

A python based notification handler for MPD to display a notification when the song changes containing the name, artist, album and cover art of the song.

![Image](images/mpd-notification.png)

_Notification as seen in Dunst_

## Usage

```
usage: mpd-notify [options]

MPD notification handler

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           Location of the mpd host (default: localhost)
  --port PORT           The port which mpd is running (default: 6600)
  --id ID               What the notification id is (default: 660)
  --music-dir MUSIC_DIR
                        The directory which mpd is playing from (default:
                        ~/Music)
  --watch               Continously show notifications on song change
                        (default: False)
  --fork                Fork process to background (default: False)

```

## Installation

### From Source

```
$ git clone https://github.com/slapelachie/mpd-notify.git
$ cd mpd-notify
$ pip install .
```

### From PyPI (pip)

```
pip3 install mpd_notify
```
