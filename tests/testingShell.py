#!/usr/bin/python3

'''
    Shell for manual testing.
    Uses similar testing commands used in scripts.

    Help for commands in shell_help.txt. You can also run the HELP command.
'''

from pathlib import Path
from testlib import HTTPTestClass
import os

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
WHITE = "\033[37m"
FAINT = "\033[2m"
RESET = "\033[0m"
INTENSITY_RESET = "\033[22m"

PARENT_PATH = Path(__file__).parent.resolve()


class Loop():
    '''
        Manages the loop of main.
    '''

    bool = True

    @classmethod
    def stop(cls):
        cls.bool = False


class TestShell(HTTPTestClass):
    '''
        Tests
    '''

    pass


def exit(*args: str) -> None:
    loop = False


def help(*args: str) -> None:
    with open(f"{PARENT_PATH}/shell_help.txt", "r") as f:
        for line in f:
            line = line.replace("<", GREEN + "<")
            if '=' in line:
                line = line.replace("=", FAINT + "-")
                line = line.replace(">", ">" + WHITE)
            else:
                line = line.replace(">", ">" + RESET)
            line += RESET
            print(line, end="")


commands = [method for method in dir(TestShell()) if method[0].isupper()]


built_ins = {
    "EXIT": Loop.stop,
    "QUIT": Loop.stop,
    "HELP": help,
    "CLEAR": lambda: os.system('clear')
}


def printHell(obj, level: int = 1, *, inside_dict=False) -> None:
    '''
        Prints in a beautiful way.
    '''

    if isinstance(obj, dict):
        len_of_obj = len(obj) - 1
        print("  " * level, end="")
        print(end="{")
        if level == 1:
            print()
        for i, key in enumerate(obj):
            if level == 1:
                print(f"  - {BLUE}'{key}'{RESET}: ")
            else:
                print(end=f"{CYAN}'{key}'{RESET}: ")
            printHell(obj[key], level + 1, inside_dict=True)
            if len_of_obj != i:
                print(end=", ")
                if level == 1:
                    print()
        print(end="}")
    elif isinstance(obj, list):
        len_of_obj = len(obj) - 1
        print(end="[")
        for i, element in enumerate(obj):
            printHell(element, level + 1, inside_dict=inside_dict)
            if len_of_obj != i:
                print(", ")
        print(end="]")
    elif isinstance(obj, str):
        if level <= 2 or not inside_dict:
            print("  " * level, end="")
            print(end=f"- {FAINT}'{obj}'{RESET}")
        else:
            print(end=f"{FAINT}'{obj}'{RESET}")
    else:
        if level <= 2 or not inside_dict:
            print("  " * level, end="")
            print(end=f"- {MAGENTA}{repr(obj)}{RESET}")
        else:
            print(end=f"{MAGENTA}{repr(obj)}{RESET}")


def runner(line: str) -> None:
    '''
        Separates line into list of args, which are list of args, then
        tries to run each command (args[0]) from the prompt.
    '''

    prompts = [prompt.split() for prompt in line.split(";")]

    for args in prompts:
        command = args[0].upper()
        if command in built_ins:
            built_ins[command](*args[1:])
        elif command in commands:
            ret = getattr(TestShell, command)(*args[1:])
            if ret:
                printHell(ret)
                print()
        else:
            raise Exception(f"  {RED}!{RESET} {command} {RED}not found{RESET}")


def main() -> None:
    '''
        Interactive shell main.
    '''

    while Loop.bool:
        try:
            line = input("$ ")
            runner(line)
        except (KeyboardInterrupt, EOFError):
            print()
            Loop.stop()
        except Exception as e:
            print(f"  {RED}! {e}{RESET}")


if __name__ == "__main__":
    main()
