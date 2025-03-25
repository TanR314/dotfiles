from ignis.widgets import Widget



# class SearchEntry(Widget.Entry)







class SearchBox(Widget.Box):
    def __init__(self):
        self.entry = Widget.Entry(
            css_classes=["Overview-Search-Entry"],
            placeholder_text="Search",
            # on_accept=lambda x: print(x.text),
            on_change=lambda x: print(x.text),
        )
        self.entry.focus()
        super().__init__(
            halign="center",
            child=[
                self.entry
                
            ]
        )


