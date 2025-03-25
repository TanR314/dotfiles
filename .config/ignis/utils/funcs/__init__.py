from ignis.utils import Utils






def Format_Time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if hours > 0:
        return f"{hours}:{minutes:02}:{seconds:02}"  # Format as HH:MM:SS
    else:
        return f"{minutes}:{seconds:02}"  # Format as MM:SS




# Widget Specific Functions


from ignis.widgets import Widget


def ToggleClass(widget, css_class):

    if widget.has_css_class(css_class):
        widget.remove_css_class(css_class)
    else:
        widget.add_css_class(css_class)


def AddClass(widget, css_class, condition):
    if condition:
        widget.add_css_class(css_class)
    else:
        widget.remove_css_class(css_class)





def AddBox(parent, child, prepend: bool = False, visible: bool = True):
    revealer = Widget.Revealer(
        child=child,
        reveal_child=False,
        transition_duration=100,
    )
    if not prepend:
        parent.append(revealer)
    else:
        parent.prepend(revealer)
    if visible:
        revealer.reveal_child=True





def RemoveAddedBox(child):
    child.parent.reveal_child = False
    Utils.Timeout(child.parent.transition_duration, lambda: child.parent.parent.remove(child.parent))












# ========================== x ============================




from collections import defaultdict


# Notification Filter
def FilterNotification(notifications):
    grouped_notifications = defaultdict(list)
    for notification in notifications:
        grouped_notifications[notification.app_name].append(notification)

    return grouped_notifications















