from ignis.utils import Utils
import os


def onFileChanged(idkWhatIsThis, path, event_type):
    generationFile = os.path.expanduser("~/.config/ignis/wallpapers/generator.py")
    SWWW_CACHE_FILE = os.path.expanduser("~/.cache/swww/eDP-1")
    WALLPAPER_FILE=Utils.exec_sh("cat " + SWWW_CACHE_FILE).stdout
    quality = 64
    scheme = "tonalspot"
    scssFile = os.path.expanduser("~/.config/ignis/styles/material/colors.scss")

    Utils.exec_sh(f"{generationFile} {WALLPAPER_FILE} {quality} {scheme} > {scssFile}")
    


Utils.FileMonitor(
    path=os.path.expanduser("~/.cache/swww/eDP-1"),
    recursive=False,
    callback=onFileChanged
)
