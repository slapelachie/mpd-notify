import notify2


class Notify:
    def __init__(self):
        self.app_name = "mpd_notify"

        notify2.init(self.app_name)

    def notify(self, title, message, icon=None):
        if icon:
            n = notify2.Notification(title, message=message, icon=icon)
        else:
            n = notify2.Notification(title, message=message)
        n.show()