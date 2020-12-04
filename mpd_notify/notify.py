import notify2


class Notify:
    def __init__(self, notification_id=660, app_name="mpd_notify"):
        self.app_name = app_name
        self.id = notification_id

        notify2.init(self.app_name)

    def notify(self, title, message, icon=None):
        if icon:
            n = notify2.Notification(title, message=message, icon=icon)
        else:
            n = notify2.Notification(title, message=message)

        n.id = self.id
        n.show()


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