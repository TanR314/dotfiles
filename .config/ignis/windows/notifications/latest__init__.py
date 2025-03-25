
from ignis.widgets import Widget
from ignis.utils import Utils
from utils.funcs import AddBox,RemoveAddedBox
from ignis.services.notifications import Notification, NotificationService


notifications = NotificationService.get_default()


from widgets.notification import NotificationBox




class NotificationPopup(Widget.Window):
    def __init__(self):
        super().__init__(
            anchor=["top"],
            namespace=f"ignis_NOTIFICATION_POPUP",
            layer="overlay",
            child=Widget.Revealer(
                child=NotificationBox(),
                reveal_child=False,
                transition_type="crossfade"
            ),
            visible=False,
            # dynamic_input_region=True,
            css_classes=["rec-unset"],
            style="min-width: 29rem;",
        )


