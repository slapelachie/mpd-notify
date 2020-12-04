import notify2


class Notify:
    def __init__(self):
        self.app_name = "mpd_notify"
        self.id = 6600

        notify2.init(self.app_name)

    def set_id(self, id):
        self.id = 6600

    def notify(self, title, message, icon=None):
        if icon:
            n = notify2.Notification(title, message=message, icon=icon)
        else:
            n = notify2.Notification(title, message=message)

        n.id = self.id
        n.show()