
from ignis.widgets import Widget



from widgets.overview import Overview
# from widgets.search_box import SearchBox







class SearchBox(Widget.Box):
    def __init__(self):
        self.entry = Widget.Entry(
            css_classes=["Overview-Search-Entry"],
            placeholder_text="Search",
            on_accept=lambda x: print(x.text),
            on_change=lambda x: print(x.text),
        )
        super().__init__(
            halign="center",
            child=[
                self.entry
                
            ]
        )








class Overview_Search(Widget.Window):
    def __init__(self):
        super().__init__(
            anchor=["top"],
            namespace="overviewsearch",

            # kb_mode = "on_demand",
            kb_mode="exclusive",
            popup=True,
            child=Widget.Box(
                vertical=True,
                child=[
                    SearchBox(),
                    Overview()
                ]
            ),
            visible=False,
            # dynamic_input_region=True,
        )
