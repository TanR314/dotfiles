from ignis.widgets import Widget

from widgets.bar.stackright.audio import AudioIndicator
from widgets.bar.stackright.network import NetworkIndicator

from windows.popupwindow import PopupWindow


from widgets.quicksettings import Quicksettings

from ..PanelButton import PanelButton




popup=PopupWindow(namespace="quicksettings",child=Quicksettings(),anchor=["top", "right"], margin_right=10)

def StackRight():

    def on_click(self):
        popup.visible = not popup.visible
        self.activate()


    MyBox = Widget.Box(
        child=[
            PanelButton(
                on_click = on_click,
                child = Widget.Box(
                    spacing=3,
                    child=[
                        AudioIndicator(),
                        NetworkIndicator(),
                    ],
                ),
            ),
        ],
    )


    return MyBox


