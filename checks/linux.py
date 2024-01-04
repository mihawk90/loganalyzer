from .vars import *
from .utils.utils import *


def getSessionTypeLine(lines):
    sessionType = search('Session Type:', lines)
    if len(sessionType) > 0:
        return sessionType[0]


def getWindowSystemLine(lines):
    windowSystem = search('Window System:', lines)
    if len(windowSystem) > 0:
        return windowSystem[0]


def checkFlatpak(lines):
    isFlatpak = search('Flatpak Runtime:', lines)

    if len(isFlatpak) > 0:
        return [LEVEL_INFO, "Flatpak",
                "You are using the Flatpak. Plugins are available as Flatpak extensions, which you can find in your Distributions Software Center or via <code>flatpak search com.obsproject.Studio</code>. Installation of external plugins is not supported."]


def checkSnapPackage(lines):
    isDistroNix = search('Distribution:', lines)

    if len(isDistroNix) <= 0:
        return

    distro = isDistroNix[0].split()
    # Snap Package logs "Ubuntu Core" as distro, so it gets split halfway
    if distro[2] == '"Ubuntu' and distro[3] == 'Core"':
        return [LEVEL_WARNING, "Snap Package",
                "You are using the Snap Package. This is a community-supported modified build of OBS Studio; please file issues on the <a href=\"https://github.com/snapcrafters/obs-studio/issues\">Snapcrafters GitHub</a>.<br><br>OBS may be unable to assist with issues arising out of the usage of this package and therefore recommends following our <a href=\"https://obsproject.com/download#linux\">Install Instructions</a>."]


def checkWayland(lines):
    isDistroNix = search('Distribution:', lines)
    isFlatpak = search('Flatpak Runtime:', lines)

    if (len(isDistroNix) <= 0) and (len(isFlatpak) <= 0):
        return

    sessionTypeLine = getSessionTypeLine(lines)
    if not sessionTypeLine:
        return

    sessionType = sessionTypeLine.split()[3]
    if sessionType != 'wayland':
        return

    if len(isDistroNix) > 0:
        distro = isDistroNix[0].split()
        if distro[2] == '"Ubuntu"' and distro[3] == '"20.04"':
            return [LEVEL_CRITICAL, "Ubuntu 20.04 under Wayland",
                    "Ubuntu 20.04 does not provide the needed dependencies for OBS to capture under Wayland.<br> So OBS is able to capture only under X11/Xorg."]

    windowSystemLine = getWindowSystemLine(lines)
    # If there is no Window System, OBS is running under Wayland
    if windowSystemLine:
        # If there is, OBS is running under XWayland
        return [LEVEL_CRITICAL, "Running under XWayland",
                "OBS is running under XWayland, which prevents OBS from being able to capture.<br>To fix that, you will need to run OBS with the following command in a terminal:<p><code>obs -platform wayland</code></p>"]

    hasNoPipewireCapture = search('[pipewire] No capture', lines)
    if len(hasNoPipewireCapture) > 0:
        return [LEVEL_CRITICAL, "No PipeWire capture on Wayland",
                """In order to capture displays or windows under Wayland, OBS requires the appropriate PipeWire capture portal for your Desktop Environment.<br><br>
                An overview of available capture portals can be found on the Arch Linux Wiki:<br>
                <a href='https://wiki.archlinux.org/title/XDG_Desktop_Portal'>XDG Desktop Portal</a><br>
                Note that the availability of Window and/or Display capture depends on your Desktop Environment's implementation of these portals."""]

    return [LEVEL_INFO, "Wayland",
            """Window and Display Captures are available via <a href='https://wiki.archlinux.org/title/XDG_Desktop_Portal'>XDG Desktop Portal</a><br>.
            Please note that the availability of captures and specific features depends on your Desktop Environment's implementation of these portals.<br><br>
            Global Keyboard Shortcuts are not currently available under Wayland."""]
