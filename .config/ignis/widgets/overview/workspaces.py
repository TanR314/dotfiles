from ignis.widgets import Widget

from ignis.utils import Utils
from gi.repository import Gtk


# self.mybox=Widget.Box(
#     style="min-height: 20px;min-width: 20px;background: red;",
# )

class MyBox(Widget.Box):
    def __init__(self):
        super().__init__(
            css_classes=["Overview-Window"],
            style="min-height: 20px;min-width: 20px;background: red;",
        )

        def onTimeout():
            self.style="min-height: 50px;min-width: 50px;background: coral;"
            print("OMG")

        Utils.Timeout(5000, lambda:onTimeout())

class Workspace(Widget.EventBox):
    def __init__(self,i):
        self._width = Utils.get_monitor(0).get_geometry().width
        self._height = Utils.get_monitor(0).get_geometry().height



        self.fixed = Gtk.Fixed()


        # def update():


        super().__init__(
            style=f"min-height: {self._height/5.5}px;min-width: {self._width/5.5}px;",
            css_classes=["Overview-Workspace"],
            # child = [Widget.Label(label="OMG")]
            child=[
                self.fixed
            ]
        )

