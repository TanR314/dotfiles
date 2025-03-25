from ignis.widgets import Widget


from utils.funcs import ToggleClass


class PanelButton(Widget.EventBox):
    def __init__(self,child,on_click=lambda box: print('bruh'), on_right_click=lambda box:print("OMG")):
        super().__init__(
            on_click=on_click,
            on_right_click=on_right_click,
            css_classes=["panel-button"],
            child=[child]
        )

    def activate(self):
        ToggleClass(self, "activated")




