from enum import Enum


class Section(str, Enum):
    # DAYS
    monday = "MONDAY"
    tuesday = "TUESDAY"
    wednesday = "WEDNESDAY"
    thursday = "THURSDAY"
    friday = "FRIDAY"
    # you should not work at these days ;)
    saturday = "SATURDAY"
    sunday = "SUNDAY"

    # OTHERS
    todo = "TODO"


class CommandEnum(str, Enum):
    ls = "ls"
    todo = "td"
    done = "dn"
    reset = "rst"
    quit = "q"
