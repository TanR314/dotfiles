from ignis.widgets import Widget
from ignis.utils import Utils


from utils.funcs import AddBox,RemoveAddedBox
# from widgets.center_widget.notification import NotificationBox
from widgets.shared_widgets.notification import NotificationWidget



from ignis.services.notifications import Notification, NotificationService


notifications = NotificationService.get_default()





class NotificationPopup(Widget.Window):
    def __init__(self):
        self.MyBox = Widget.Box(
            vertical=True,
            style="min-width: 400px;"
        )
        super().__init__(
            anchor=["top"],
            layer="top",
            namespace="NotificationPopup",
            child=self.MyBox,  # do not set Widget.Revealer as a direct child!
        )


        notifications.connect("new_popup", lambda x,notification: self.on_notified(notification))


    def on_notified(self, notification):
        self.visible=True
        if len(self.MyBox.child) >= 1:
            revealer = Widget.Revealer(
                child=NotificationWidget(notification, "dismissed",self),
                reveal_child=False,
                transition_duration=100,
            )
            self.MyBox.append(revealer)
            self.MyBox.child[0].child._notification.dismiss()
            def reveal():
                revealer.reveal_child=True
            Utils.Timeout(
                100,
                reveal
            )
        else:
            AddBox(self.MyBox, NotificationWidget(notification, "dismissed",self))
