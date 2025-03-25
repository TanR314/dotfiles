from ignis.widgets import Widget

from gi.repository import GLib





class PopupWindow(Widget.Window):
    def __init__(
        self,
        child,
        namespace,
        css_classes=[""],
        anchor=["top"],
        margin_top=0,
        margin_bottom=0,
        margin_right=0,
        margin_left=0,
        *kwargs
    ):
        self.MyBox = Widget.Box(
            css_classes=["PopupWindow"],
            child=[child]
        )
        super().__init__(
            anchor=anchor,
            visible=False,
            popup=True,
            layer="top",
            namespace=namespace,
            css_classes=css_classes,
            child=self.MyBox,  # do not set Widget.Revealer as a direct child!
            margin_right=margin_right,
            margin_top=margin_top,
            margin_left=margin_left,
            margin_bottom=margin_bottom,
        )

