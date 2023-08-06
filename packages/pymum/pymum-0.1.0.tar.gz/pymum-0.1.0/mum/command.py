from configparser import SectionProxy
from datetime import date
from itertools import zip_longest

from rich.console import Console
from rich.table import Table

from mum.constants import MAP_INT_TO_WEEKDAY
from mum.enums import CommandEnum, Section
from mum.todo_file import TodoFile


class Command:
    def __init__(self, todo_file: TodoFile, command: str, console: Console) -> None:
        self._todo_file = todo_file
        self._command: list[str] = command.split(" ")
        self._console = console

    def _ls_all(self, table: Table) -> None:
        for name in [member.lower().capitalize() for member in Section]:
            table.add_column(name)

        result = []
        for section in [self._todo_file.get_section(member) for member in Section]:
            row = []
            for value in section.values():
                row.append(value)
            result.append(row)

        for row in zip_longest(*result):
            table.add_row(*row)

    def _ls(self, command: list[str], table: Table) -> bool:
        if not command:
            self._ls_all(table)
            return True

        commands = [section.lower().capitalize() for section in Section]
        fst_command = command[0].lower().capitalize()
        if fst_command not in commands:
            return False

        table.add_column(fst_command)
        section = self._todo_file.get_section(Section[fst_command.lower()])
        for key, value in section.items():
            if fst_command == Section.todo.value.lower().capitalize():
                table.add_row(f"{key}: {value}")
                continue

            table.add_row(value)

        return True

    def _rst(self) -> None:
        self._todo_file.bootstrap_todo_file()

    @staticmethod
    def _max_section_number(section: SectionProxy) -> int:
        return int(max(sorted(section.keys()))) if section else 0

    def _dn(self, text: str) -> bool:
        if not text:
            return False

        day = MAP_INT_TO_WEEKDAY[date.today().weekday()]
        day_section = self._todo_file.get_section(Section[day])
        day_section[str(self._max_section_number(day_section) + 1)] = text
        return True

    def _td(self, command: list[str]) -> bool:
        if not command:
            return False

        if command[0] == "dn":
            if len(command) != 2 or not command[1].isnumeric():
                return False

            removed = self._todo_file.get_section(Section.todo).pop(command[1], None)
            return self._dn(removed)

        section = self._todo_file.get_section(Section.todo)
        section[str(self._max_section_number(section) + 1)] = " ".join(command)
        return True

    def run_command(self) -> bool:
        fst_command = self._command[0].lower()
        tail = self._command[1 : len(self._command)]
        if fst_command == CommandEnum.ls:
            table = Table()
            retval = self._ls(tail, table)
            self._console.print(table)
            return retval

        if fst_command == CommandEnum.reset:
            self._rst()
            return True

        if fst_command == CommandEnum.done:
            retval = self._dn(" ".join(tail))
            self._todo_file.write_config_to_file()
            return retval

        if fst_command == CommandEnum.todo:
            retval = self._td(tail)
            self._todo_file.write_config_to_file()
            return retval

        return False
