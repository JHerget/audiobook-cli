from audiobook_api import AudiobookApi
from .types import CommandOptions
from .helpers import table, input_number, input_path, input_command, extract_and_repermission
from tqdm import tqdm

def list_authors(api: AudiobookApi, commands: CommandOptions):
    response = api.get_authors()
    authors = []

    if response.ok: 
        authors = response.json()["authors"]

    authors_table = table(
        title="AUTHORS",
        data=[(str(index), author["name"]) for index, author in enumerate(authors)]
    )
    print(authors_table)

    cmd = input_command(get_table_data(commands))
    action = commands[cmd]["action"]

    if cmd == "lb":
        index = input_number(range(0, len(authors) - 1))
        action(api, author=authors[index]["name"])
    else:
        action(api)

def list_books(api: AudiobookApi, commands: CommandOptions, author: str | None = None):
    response = api.get_books()
    books = []

    if response.ok:
        books = response.json()["results"]

        if author:
            books = [book for book in books if book["media"]["metadata"]["authorName"] == author]

    books_table = table(
        title="BOOKS",
        data=[(str(index), book["media"]["metadata"]["title"]) for index, book in enumerate(books)]
    )
    print(books_table)

    cmd = input_command(get_table_data(commands))
    action = commands[cmd]["action"]

    if cmd == "db":
        index = input_number(range(0, len(books) - 1))
        action(api, book_id=books[index]["id"])
    else:
        action(api)

def download_book(api: AudiobookApi, commands: CommandOptions, book_id: str):
    download_path = input_path()
    progress_bar = tqdm(total=100, unit="%", leave=True)
    
    def notify_progress(percent_complete: float):
        completion_whole = int(percent_complete * 100)

        if completion_whole > progress_bar.n:
            progress_bar.update(completion_whole - progress_bar.n)

        if completion_whole >= 100:
            print("Download complete!")
            progress_bar.close()

    file_path = api.download_book(
        book_id=book_id,
        download_path=download_path,
        notify=notify_progress
    )
    extract_and_repermission(file_path)
    
    cmd = input_command(get_table_data(commands))
    action = commands[cmd]["action"]

    action(api)

def get_table_data(options: CommandOptions):
    return [(cmd, options[cmd]["description"]) for cmd in options]
