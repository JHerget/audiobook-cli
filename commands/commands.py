from .types import Command, CommandDetails
from .actions import list_authors, list_books, download_book

commands: dict[Command, CommandDetails] = {
    "la": {
        "description": "list authors",
        "action": lambda api: list_authors(api, get_sub_options("la")),
        "sub_commands": ["lb", "b", "q"]
    },
    "lb": {
        "description": "list books",
        "action": lambda api, author=None: list_books(api, get_sub_options("lb"), author=author),
        "sub_commands": ["db", "b", "q"]
    },
    "db": {
        "description": "download book",
        "action": lambda api, book_id: download_book(api, get_sub_options("db"), book_id=book_id),
        "sub_commands": ["b", "q"]
    },
    "q": {
        "description": "quit",
        "action": lambda _: quit(),
        "sub_commands": []
    },
    "b": {
        "description": "go back",
        "action": lambda _: None,
        "sub_commands": []
    }
}

main_commands_data = [(cmd, commands[cmd]["description"]) for cmd in ["la", "lb", "q"]]

def get_sub_options(command):
    sub_commands = commands[command]["sub_commands"]
    return { cmd: commands[cmd] for cmd in sub_commands }
