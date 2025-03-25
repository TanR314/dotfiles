import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk

# Assume these are provided by your Ignis installation:
from ignis import Widget, Variable, App, Hyprland, Utils
from ignis.utils import exec_async  # Example helper function
from commonutils.icons import iconExists, substitute
from commondata.hyprlanddata import monitors
from commonwidgets.materialicon import MaterialIcon
from widgetutils.cursorhover import setup_cursor_hover_grab
from actions import dump_to_workspace, swap_workspace

# Global reactive variable for overview updates.
overview_tick = Variable(False)

# Some constants from the original code:
NUM_OF_WORKSPACES_SHOWN = userOptions["overview"]["numOfCols"] * userOptions["overview"]["numOfRows"]
TARGET = [Gtk.TargetEntry.new('text/plain', Gtk.TargetFlags.SAME_APP, 0)]

# --- Helper: Context Menu for Workspace Actions ---
def context_menu_workspace_array(label, action_func, this_workspace):
    def setup_menu_item(menu_item):
        submenu = Gtk.Menu.new()
        submenu.get_style_context().add_class("menu")
        offset = ((Hyprland.active.workspace.id - 1) // NUM_OF_WORKSPACES_SHOWN) * NUM_OF_WORKSPACES_SHOWN
        start_workspace = offset + 1
        end_workspace = start_workspace + NUM_OF_WORKSPACES_SHOWN - 1
        for i in range(start_workspace, end_workspace + 1):
            # Use default argument trick so i is captured correctly
            def on_activate(btn, i=i):
                action_func(this_workspace, i)
                overview_tick.set_value(not overview_tick.get_value())
            button = Gtk.MenuItem.new_with_label(f"Workspace {i}")
            button.connect("activate", on_activate)
            submenu.append(button)
        menu_item.set_reserve_indicator(True)
        menu_item.set_submenu(submenu)
    return Widget.MenuItem(label=label, setup=setup_menu_item)

# --- Helper: Create a Window Widget from a Client ---
def window_widget(client, screen_coords):
    # Unpack client data (expecting client as a dict)
    address = client["address"]
    x, y = client["at"]
    w, h = client["size"]
    ws_id = client["workspace"]["id"]
    c = client.get("class", "")
    initial_class = client.get("initialClass", "")
    monitor_index = client["monitor"]
    title = client["title"]
    xwayland = client.get("xwayland", False)

    # Condition to reveal extra info:
    reveal_info_condition = min(w, h) * userOptions["overview"]["scale"] > 70
    if w <= 0 or h <= 0 or (c == "" and title == ""):
        return None

    # Adjust positions relative to screen coordinates
    if screen_coords["x"] != 0:
        x -= screen_coords["x"]
    if screen_coords["y"] != 0:
        y -= screen_coords["y"]

    # Offscreen adjustments
    if x + w <= 0:
        x += (x // monitors[monitor_index]["width"]) * monitors[monitor_index]["width"]
    elif x < 0:
        w = x + w
        x = 0
    if y + h <= 0:
        y += (y // monitors[monitor_index]["height"]) * monitors[monitor_index]["height"]
    elif y < 0:
        h = y + h
        y = 0

    # Ensure monitor index is valid
    if monitor_index >= len(monitors):
        monitor_index = len(monitors) - 1

    # Truncate if offscreen
    if x + w > monitors[monitor_index]["width"]:
        w = monitors[monitor_index]["width"] - x
    if y + h > monitors[monitor_index]["height"]:
        h = monitors[monitor_index]["height"] - y

    if not c:
        c = initial_class
    icon_name = substitute(c)
    if iconExists(icon_name):
        app_icon = Widget.Icon(icon=icon_name,
                               size=min(w, h) * userOptions["overview"]["scale"] / 2.5)
    else:
        app_icon = MaterialIcon('terminal', 'gigantic',
                                css=f"font-size: {min(w, h) * userOptions['overview']['scale'] / 2.5}px")

    # Define event handlers
    def on_clicked(button):
        Hyprland.message_async(f"dispatch focuswindow address:{address}")
        App.close_window("overview")

    def on_middle_click_release():
        Hyprland.message_async(f"dispatch closewindow address:{address}")

    def on_secondary_click(button):
        button.toggle_class_name("overview-tasks-window-selected", True)
        menu = Widget.Menu(
            className="menu",
            children=[
                Widget.MenuItem(
                    child=Widget.Label(xalign=0, label="Close (Middle-click)"),
                    on_activate=lambda: Hyprland.message_async(f"dispatch closewindow address:{address}")
                ),
                context_menu_workspace_array("Dump windows to workspace", dump_to_workspace, int(ws_id)),
                context_menu_workspace_array("Swap windows with workspace", swap_workspace, int(ws_id))
            ]
        )
        menu.connect("deactivate", lambda: button.toggle_class_name("overview-tasks-window-selected", False))
        menu.connect("selection-done", lambda: button.toggle_class_name("overview-tasks-window-selected", False))
        menu.popup_at_widget(button.get_parent(), Gdk.Gravity.SOUTH, Gdk.Gravity.NORTH, None)
        button.connect("destroy", lambda: menu.destroy())

    def setup_button(button):
        setup_cursor_hover_grab(button)
        button.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, TARGET, Gdk.DragAction.MOVE)
        button.drag_source_set_icon_name(substitute(c))
        button.connect("drag-begin", lambda btn: btn.toggle_class_name("overview-tasks-window-dragging", True))
        def on_drag_data_get(btn, context, data):
            data.set_text(address, len(address))
            btn.toggle_class_name("overview-tasks-window-dragging", False)
        button.connect("drag-data-get", on_drag_data_get)

    # Build the window button widget
    return Widget.Button(
        attribute={
            "address": address,
            "x": x, "y": y, "w": w, "h": h, "ws": ws_id,
            "updateIconSize": lambda self: setattr(app_icon, "size",
                                                    min(self.attribute["w"], self.attribute["h"]) * userOptions["overview"]["scale"] / 2.5)
        },
        className="overview-tasks-window",
        hpack="start",
        vpack="start",
        css=f"""
            margin-left: {round(x * userOptions['overview']['scale'])}px;
            margin-top: {round(y * userOptions['overview']['scale'])}px;
            margin-right: -{round((x + w) * userOptions['overview']['scale'])}px;
            margin-bottom: -{round((y + h) * userOptions['overview']['scale'])}px;
        """,
        onClicked=on_clicked,
        onMiddleClickRelease=on_middle_click_release,
        onSecondaryClick=on_secondary_click,
        child=Widget.Box(
            homogeneous=True,
            child=Widget.Box(
                vertical=True,
                vpack="center",
                children=[
                    app_icon,
                    Widget.Revealer(
                        transition="slide_right",
                        revealChild=reveal_info_condition,
                        child=Widget.Revealer(
                            transition="slide_down",
                            revealChild=reveal_info_condition,
                            child=Widget.Label(
                                maxWidthChars=1,
                                truncate="end",
                                className="margin-top-5 " + ("txt txt-italic" if xwayland else "txt"),
                                css=f"""
                                    font-size: {min(monitors[monitor_index]['width'], monitors[monitor_index]['height']) * userOptions['overview']['scale'] / 14.6}px;
                                    margin: 0px {min(monitors[monitor_index]['width'], monitors[monitor_index]['height']) * userOptions['overview']['scale'] / 10}px;
                                """,
                                label=(f"{c}: {title}" if len(title) <= 1 else title)
                            )
                        )
                    )
                ]
            )
        ),
        tooltipText=f"{c}: {title}",
        setup=setup_button
    )

# --- Helper: Workspace Container Widget ---
def workspace_widget(index):
    # 'fixed' will be a container that supports putting/moving child widgets.
    fixed = Widget.Box(attribute={
        "put": lambda widget, x, y: widget.set_css(f"""
            margin-left: {round(x)}px;
            margin-top: {round(y)}px;
            margin-right: -{round(x + widget.attribute["w"] * userOptions["overview"]["scale"])}px;
            margin-bottom: -{round(y + widget.attribute["h"] * userOptions["overview"]["scale"])}px;
        """),
        "move": lambda widget, x, y: widget.set_css(f"""
            margin-left: {round(x)}px;
            margin-top: {round(y)}px;
            margin-right: -{round(x + widget.attribute["w"] * userOptions["overview"]["scale"])}px;
            margin-bottom: -{round(y + widget.attribute["h"] * userOptions["overview"]["scale"])}px;
        """)
    })

    # Workspace number label widget
    def create_workspace_number(idx):
        label = Widget.Label(
            className="overview-tasks-workspace-number",
            label=str(idx),
            css=f"""
                margin: {min(monitors[overview_monitor]['width'], monitors[overview_monitor]['height']) * userOptions['overview']['scale'] * userOptions['overview']['wsNumMarginScale']}px;
                font-size: {monitors[overview_monitor]['height'] * userOptions['overview']['scale'] * userOptions['overview']['wsNumScale']}px;
            """
        )
        # Hook into Hyprland.active.workspace to update when needed.
        label.hook(Hyprland.active.workspace, lambda self: setattr(self, "label", str(
            ((Hyprland.active.workspace.id - 1) // NUM_OF_WORKSPACES_SHOWN) * NUM_OF_WORKSPACES_SHOWN + idx)))
        return label

    workspace_number = create_workspace_number(index)
    event_box = Widget.EventBox(
        hexpand=True,
        onPrimaryClick=lambda: (Hyprland.message_async(f"dispatch workspace {index}"), App.close_window("overview")),
        setup=lambda eb: (
            eb.drag_dest_set(Gtk.DestDefaults.ALL, TARGET, Gdk.DragAction.COPY),
            eb.connect('drag-data-received', lambda _w, _c, _x, _y, data: 
                       Hyprland.message_async(f"dispatch movetoworkspacesilent {index},address:{data.get_text()}") or overview_tick.set_value(not overview_tick.get_value()))
        ),
        child=Widget.Overlay(
            child=Widget.Box({}),
            overlays=[workspace_number, fixed]
        )
    )
    container = Widget.Box(
        className="overview-tasks-workspace",
        vpack="center",
        css=f"""
            min-width: {1 + round(monitors[overview_monitor]['width'] * userOptions['overview']['scale'])}px;
            min-height: {1 + round(monitors[overview_monitor]['height'] * userOptions['overview']['scale'])}px;
        """,
        children=[event_box]
    )

    # Define methods to clear, set, and unset clients from this workspace.
    def clear_clients():
        offset = ((Hyprland.active.workspace.id - 1) // NUM_OF_WORKSPACES_SHOWN) * NUM_OF_WORKSPACES_SHOWN
        for addr, client_widget in list(client_map.items()):
            if (client_widget.attribute["ws"] <= offset or
                client_widget.attribute["ws"] > offset + NUM_OF_WORKSPACES_SHOWN or
                client_widget.attribute["ws"] == offset + index):
                client_widget.destroy()
                del client_map[addr]

    def set_client(client_json, screen_coords):
        # If already exists, update dimensions; otherwise create new window widget.
        widget_existing = client_map.get(client_json["address"])
        if widget_existing:
            if widget_existing.attribute.get("ws") != client_json["workspace"]["id"]:
                widget_existing.destroy()
                del client_map[client_json["address"]]
            else:
                widget_existing.attribute["w"] = client_json["size"][0]
                widget_existing.attribute["h"] = client_json["size"][1]
                widget_existing.attribute["updateIconSize"](widget_existing)
                fixed.attribute["move"](widget_existing,
                                          max(0, client_json["at"][0] * userOptions["overview"]["scale"]),
                                          max(0, client_json["at"][1] * userOptions["overview"]["scale"]))
                return
        new_win = window_widget(client_json, screen_coords)
        if new_win is None:
            return
        fixed.attribute["put"](new_win,
                                 max(0, new_win.attribute["x"] * userOptions["overview"]["scale"]),
                                 max(0, new_win.attribute["y"] * userOptions["overview"]["scale"]))
        client_map[client_json["address"]] = new_win

    def unset_client(client_address):
        widget_existing = client_map.get(client_address)
        if widget_existing:
            widget_existing.destroy()
            del client_map[client_address]

    # Attach these methods to the container (or fixed) if desired.
    container.clear = clear_clients
    container.set_client = set_client
    container.unset_client = unset_client
    container.show_clients = lambda: fixed.show_all()
    return container

# --- Helper: Overview Row (a row of workspace containers) ---
def overview_row(start_workspace, workspaces, window_name="overview"):
    # Create a box with one workspace widget per column.
    children = [workspace_widget(i) for i in range(start_workspace, start_workspace + workspaces)]
    box = Widget.Box(
        children=children,
        attribute={
            "workspaceGroup": (Hyprland.active.workspace.id - 1) // NUM_OF_WORKSPACES_SHOWN,
            "monitorMap": [],
            "getMonitorMap": lambda self: exec_async("hyprctl -j monitors").then(
                lambda mon_str: setattr(self, "monitorMap", {item["id"]: {"x": item["x"], "y": item["y"]} for item in (json.loads(mon_str))})
            ),
            "update": lambda self: update_overview_box(self, start_workspace, workspaces, window_name),
            "updateWorkspace": lambda self, wid: update_workspace(self, wid, start_workspace, workspaces)
        },
        setup=lambda box: (
            box.attribute["getMonitorMap"](box),
            box.hook(overview_tick, lambda b: b.attribute["update"](b)),
            box.hook(Hyprland, lambda b, client_addr: b.attribute["updateWorkspace"](b, Hyprland.getClient(client_addr)["workspace"]["id"]), "client-removed"),
            box.hook(Hyprland, lambda b, client_addr: b.attribute["updateWorkspace"](b, Hyprland.getClient(client_addr)["workspace"]["id"]), "client-added"),
            box.hook(Hyprland.active.workspace, lambda b: (
                b.attribute["update"](b) if (((Hyprland.active.workspace.id - 1) // NUM_OF_WORKSPACES_SHOWN)
                                              != b.attribute["workspaceGroup"]) else None,
                setattr(b.attribute, "workspaceGroup", (Hyprland.active.workspace.id - 1) // NUM_OF_WORKSPACES_SHOWN)
            )),
            box.hook(App, lambda b, name, visible: b.attribute["update"](b) if (name == "overview" and visible) else None)
        )
    )
    return box

# --- Assemble the Overview Widget ---
def build_overview(overview_monitor=0):
    rows = []
    for row in range(userOptions["overview"]["numOfRows"]):
        start_ws = 1 + row * userOptions["overview"]["numOfCols"]
        rows.append(overview_row(start_ws, userOptions["overview"]["numOfCols"]))
    overview_box = Widget.Box(vertical=True, className="overview-tasks", children=rows)
    return Widget.Revealer(
        revealChild=True,
        hpack="center",
        transition="slide_down",
        transitionDuration=userOptions["animations"]["durationLarge"],
        child=overview_box
    )

# The module returns the built overview widget.
overview_widget = build_overview(overview_monitor=0)
