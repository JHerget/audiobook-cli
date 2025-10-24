from typing import TypedDict, Callable

Command = str
class CommandDetails(TypedDict):
    description: str
    action: Callable
    sub_commands: list[Command] 
CommandOptions = dict[Command, CommandDetails]

OptionName = str
OptionDescription = str
TableData = list[tuple[OptionName, OptionDescription]]
