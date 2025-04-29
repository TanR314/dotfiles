from ignis.widgets import Widget

RoundCorners = Widget.Window(
    namespace="RoundCorners",
    anchor=["top","bottom","left","right"],
    dynamic_input_region=True,
    input_width=0,
    input_height=0,
    layer="top",
    child=Widget.Box(
        hexpand = True,
        vexpand = True,
        css_classes=["roundcorners"],
        child=[
            Widget.Box(
                hexpand = True,
                vexpand = True,
                css_classes=["background"]
            )
        ]
    )
)

