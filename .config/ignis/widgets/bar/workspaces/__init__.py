from ignis.services.hyprland import HyprlandService
hyprland = HyprlandService.get_default()


from utils.funcs import AddClass


from ignis.widgets import Widget


from ..PanelButton import PanelButton


from windows.overview_search import Overview_Search


from ignis.utils import Utils

def buttonSetup(widget,i):
    AddClass(widget,"active-workspace",i==hyprland.active_workspace["id"])
    occupied = False
    for x in hyprland.workspaces: 
        if i==x["id"]:
            occupied = True
            break
    AddClass(widget,"occupied-workspace",occupied)




class numberToButtons(Widget.Label):
    def __init__(self, i):
        super().__init__(
            label=str(i),
            valign = "center",
            css_classes=["workspace-button"],
            setup=lambda self: hyprland.connect("notify::workspaces",lambda x,y: buttonSetup(self,i)),
        )



overview_search = Overview_Search()


def on_click(self):
    overview_search.visible = not overview_search.visible
    # Utils.exec_sh_async("uwsm app -- fuzzel --launch-prefix=\"uwsm app -- \"; hyprctl layers", lambda x: print(x.stdout))
    # print(Utils.exec_sh_async("hyprctl clients"))
    # Utils.exec_sh_async("hyprctl clients")
    # print("OMG")




class Workspaces(Widget.Box):
    def __init__(self):
        super().__init__(
            # css_classes=["workspaces"],
            # child=map(numberToButtons, range(1,8))
            child=[
                PanelButton(
                    # on_click=on_click,
                    on_right_click = on_click,
                    child=Widget.Box(
                        css_classes=["workspaces"],
                        child=map(numberToButtons, range(1,8))
                    )
                )
            ]
        )
# workspaces
