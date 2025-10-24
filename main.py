import argparse
import audiobook_api
import commands

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", "-u")
    parser.add_argument("--password", "-p")

    args = parser.parse_args()

    if not args.username:
        args.username = input("Username: ")

    if not args.password:
        args.password = input("Password: ")
    
    api = audiobook_api.login(
        username=args.username,
        password=args.password
    )

    while True:
        cmd = commands.input_command(commands.main_commands_data)
        action = commands.all[cmd]["action"]

        action(api)

