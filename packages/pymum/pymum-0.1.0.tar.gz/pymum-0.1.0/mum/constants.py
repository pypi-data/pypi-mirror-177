from pathlib import Path

CONFIG_FILE_PATH = Path(Path.home() / ".config/mum")
PROMPT = "mum> "

# different langs... I need them in english
MAP_INT_TO_WEEKDAY = {
    0: "monday",
    1: "tuesday",
    2: "wednesday",
    3: "thursday",
    4: "friday",
    5: "saturday",
    6: "sunday",
}
