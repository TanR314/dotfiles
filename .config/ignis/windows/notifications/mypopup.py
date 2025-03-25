from ignis.widgets import Widget
from ignis.services.notifications import NotificationsService

notifications = NotificationsService.get_default()




class NotificationContainer(Widget.Box):
    def __init__(self):
        self.bruh = "text"

        super().__init__(
        )



