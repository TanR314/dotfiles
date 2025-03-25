from gi.repository import Gtk, GObject, GLib
from ignis.base_widget import BaseWidget
from ignis.widgets import Widget

class Popover(Gtk.Popover, BaseWidget):
    __gtype_name__ = "IgnisWIDGET_NAME"
    __gproperties__ = {**BaseWidget.gproperties}  # this need to inherit properties from BaseWidget

    def __init__(self, **kwargs):  # accept keyword arguments
        BaseWidget.__init__(self,visible=False, **kwargs)  # this sets all properties transferred to kwargs



class SlidePopupWindow(Popover):
    def __init__(self, child, **kwargs):
        self.revealer = Widget.Revealer(
            child=child,
            transition_duration=100,
            # transition_type="crossfade",
            reveal_child=False, # Whether child is revealed.
        )

        super().__init__(
            style="min-height: 1px; min-width: 1px;",
            valign="center",
            vexpand=False,
            halign="center",
            hexpand=False,
            child=self.revealer,
            has_arrow = False,
            autohide=False,
            css_classes=["SlidePopupWindow"],
        )

    def reveal(self):
        self.popup()
        self.revealer.reveal_child = True
    
    def hide(self):
        self.revealer.reveal_child = False
        def popoverhide():
            self.popdown()
        GLib.timeout_add(94,popoverhide)

    def toggle(self):
        if self.get_visible():
            self.hide()
        else:
            self.reveal()





