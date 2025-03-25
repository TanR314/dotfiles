from ignis.widgets import Widget
from .workspaces import Workspace


class Overview(Widget.Box):
    def __init__(self):
        super().__init__(
            css_classes = ["PopupWindow"],
            vertical=True,
            child=[
                Widget.Box(
                    child=[
                        Workspace(i)
                        for i in range(1,6)
                    ]
                ),

                Widget.Box(
                    child=[
                        Workspace(i)
                        for i in range(6,11)
                    ]
                )
                # Workspace(i)
                # for i in range(1,10)
            ]
        )
