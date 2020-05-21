from typing import NoReturn

from game.database import target_details
from termcolor import cprint


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

        mars = target_details("mars")
        if mars['hacked'] == 1:
            cprint("Mission successful", "green")
            return

        ports = mars['ports']

        if ports['443']['state'] == "open" or ports['80']['state'] == "open":
            cprint("It's not over yet, the webserver is still targetable", "cyan")
            return

        cprint("Mission failed, the webserver blocked your attempts at taking it down!", "red")

        cprint("Reset with the init command and try again.", "cyan")

    else:
        cprint(mission, "cyan")
