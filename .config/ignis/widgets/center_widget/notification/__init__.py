from ignis.widgets import Widget

from ignis.utils import Utils
from utils.funcs import AddBox,RemoveAddedBox

from ignis.services.notifications import Notification, NotificationService

from widgets.shared_widgets.notification import NotificationWidget


notifications = NotificationService.get_default()





class PlaceHolderBox(Widget.Box):
    def __init__(self):
        super().__init__(
            css_classes=[
                "NotificationsContainerPlaceHolder"
            ],
            child=[
                Widget.Label(
                    label="No Notification",
                    halign="center",
                    hexpand=True,
                    visible = notifications.bind("notifications", lambda x: False if len(x) > 0 else True)
                )
            ]

        )







class NotificationBox(Widget.Box):
    def __init__(self):
        self.MyBox = Widget.Box(

            vertical=True,
            css_classes=["NotificationsContainer"],
            child=[
            ],
            setup=lambda mybox: notifications.connect(
                "new_popup",
                lambda x, notification: self.__on_notified(notification),
            )
        )
        super().__init__(
            vertical=True,
            css_classes=["NotificationBox"],
            child=[
                Widget.Box(
                    css_classes=["NotificationBoxTop"],
                    child=[
                        Widget.Label(
                            label="Notifications",
                            css_classes=["NotificationsTitle"],
                            hexpand=True,
                            halign="start",
                        ),
                        Widget.Button(label="Clear All", on_click=lambda x: notifications.clear_all()),
                    ]
                ),
                Widget.Overlay(
                    child=PlaceHolderBox(),
                    overlays=[
                        Widget.Scroll(
                            child=self.MyBox
                        )
                    ]
                )
            ],
        )

        for notification in notifications.notifications:
            self.__on_notified(notification)



    def __on_notified(self, notification: Notification):
        MyPopup=NotificationWidget(notification)
        AddBox(self.MyBox,MyPopup,True)

