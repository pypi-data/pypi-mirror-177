from configparser import ConfigParser, SectionProxy
from typing import Optional

from mum.constants import CONFIG_FILE_PATH
from mum.enums import Section


class TodoFile:
    def __init__(self) -> None:
        self._config = self._get_todo_file()

    def write_config_to_file(self, config: Optional[ConfigParser] = None) -> None:
        if config is not None:
            self._config = config

        with CONFIG_FILE_PATH.open("w") as conf_file:
            self._config.write(conf_file)

    def bootstrap_todo_file(self) -> ConfigParser:
        config = ConfigParser()
        for section in Section:
            config[section.value] = {}

        self.write_config_to_file(config)
        return config

    def _get_todo_file(self) -> ConfigParser:
        if not CONFIG_FILE_PATH.exists():
            return self.bootstrap_todo_file()

        config = ConfigParser()
        config.read(CONFIG_FILE_PATH.expanduser())
        sections = config.sections()
        sections.sort()

        expected = [member.value for member in Section]
        expected.sort()

        if expected != sections:
            return self.bootstrap_todo_file()

        return config

    def get_section(self, section: Section) -> SectionProxy:
        return self._config[section]

    def get_sections(self) -> list[str]:
        return self._config.sections()
