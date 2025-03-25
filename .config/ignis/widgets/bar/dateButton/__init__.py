import datetime
from ignis.widgets import Widget
from ignis.utils import Utils
from ignis.variable import Variable


from widgets.center_widget.notification import NotificationBox
from windows.popupwindow import PopupWindow


from ..PanelButton import PanelButton


current_time = Variable(
    value=Utils.Poll(1000, lambda x: datetime.datetime.now().strftime("%I:%M %p - %A %d")).bind(
        "output"
    )
)


popup=PopupWindow(namespace="centerWidget",child=NotificationBox())


def on_click(self):
    self.activate()
    popup.visible=not popup.visible


class DateButton(Widget.Box):
    def __init__(self):
        super().__init__(
            child=[
                PanelButton(
                    on_click = on_click,
                    child = Widget.Label(label=current_time.bind("value")),
                ),
            ]
        )
