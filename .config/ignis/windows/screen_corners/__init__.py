from ignis.widgets import Widget

RoundCorners = Widget.Window(
    namespace="RoundCorners",
    anchor=["top","bottom","left","right"],
    dynamic_input_region=True,
    layer="bottom",
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

