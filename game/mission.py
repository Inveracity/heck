from typing import NoReturn

from game.database import target_details
from termcolor import cprint


def is_port_open(target: str, port: str) -> bool:
    tgt = target_details(target)

    ports = tgt['ports']

    if ports[port]['state'] == "open":
        return True
    return False


def is_hacked(target: str) -> bool:
    tgt = target_details(target)
    return tgt['hacked']


def mission_fail(message: str) -> NoReturn:
    cprint("Mission Failed", "red")
    cprint(message, "yellow")
    cprint("Reset with the init command and try again.", "cyan")


def mission_success(message: str) -> NoReturn:
    cprint("Mission Succeeded", "green")
    cprint(message, "yellow")
    cprint("github.com/inveracity/heck", "cyan")


def level_one(status: bool = False) -> NoReturn:
    mission = """
Mission briefing:
    In an attempt to subdue public unrest over
    undemocratic hijacking of presidency the
    sitting fascist president hired ENC0RP to
    build a voting website.

    Inside sources reveal the service only registers
    votes for the fascist leader. This is unlawful
    and must be stopped.

Goal:
    Make the webserver unavailable to the public.

    Avoid getting detected by the sentinel as it
    will lock you out entirely.
    """

    if status:
        if is_hacked("mars"):
            mission_success("You managed to block the website long enough for the election to be a total failure!")
            return

        if not is_port_open("warrior", "16660"):
            mission_fail("The sentinel is now blocking you")
            return

        if any([is_port_open("mars", "443"), is_port_open("mars", "80")]):
            cprint("It's not over yet, the webserver is still targetable", "cyan")
            return

        mission_fail("the webserver blocked your attempts at taking it down!")

    else:
        cprint(mission, "cyan")
