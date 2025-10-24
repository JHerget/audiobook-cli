from .types import TableData
from os import path, listdir, chmod, mkdir
import zipfile

def table(title: str, data: TableData, pad_len: int = 1):
    opt_len = max([len(opt) for opt, _ in data])
    desc_len = max([len(desc) for _, desc in data])
    padding = ' '*pad_len
    h_divider = f"+{'-'*(opt_len + pad_len*2)}+{'-'*(desc_len + pad_len*2)}+"
    
    table_string = f"{h_divider}\n|{padding}{title}{' '*(len(h_divider) - len(title) - pad_len - 2)}|\n{h_divider}\n"

    for opt, desc in data:
        table_string += f"|{padding}{opt}{' '*(opt_len - len(opt))}{padding}|{padding}{desc}{' '*(desc_len - len(desc))}{padding}|\n{h_divider}\n"

    return table_string

def input_number(input_range: range):
    number = None

    while number not in input_range:
        str_input = input("Option: ")

        try:
            number = int(str_input)
        except:
            number = None

    return number if number else 0

def input_path():
    input_path = None

    while not input_path or not path.isdir(input_path):
        input_path = input("Download path: ")

    return input_path

def input_command(table_data: TableData):
    cmds_table = table(title="COMMANDS", data=table_data)
    options = [cmd for cmd, _ in table_data]
    command = None

    while command not in options:
        print(cmds_table)
        command = input("Command: ").strip().lower()

    return command

def extract_and_repermission(file_path: str):
    if not zipfile.is_zipfile(file_path):
        return

    extracted_path = file_path.replace(".zip", "")
    if not path.isdir(extracted_path):
        mkdir(extracted_path)

    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(extracted_path)
    
    files = listdir(extracted_path) if path.isdir(extracted_path) else []
    for file in files:
        full_path = f"{extracted_path}/{file}"
        if path.isfile(full_path):
            chmod(full_path, 0o755)
