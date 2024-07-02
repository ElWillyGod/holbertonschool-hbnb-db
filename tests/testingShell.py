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


def runner(line: str) -> None:
    '''
        Separates line into list of args, which are list of args, then
        tries to run each command (args[0]) from the prompt.
    '''

    prompts = [prompt.split() for prompt in line.split(";")]

    # Built-in commands must take a list of positional args.
    # All commands must be uppercase. ("Except clear")
    commands: dict[str: function] = {
        "exit": Loop.stop,
        "EXIT": Loop.stop,  # Synonim
        "help": help,
        "HELP": help,  # Synonim
        "clear": lambda: os.system('clear'),

        "CHANGE_URL": TestShell.CHANGE_URL,
        "CHANGE_URL_TO_FLASK": TestShell.CHANGE_URL_TO_FLASK,
        "CHANGE_URL_TO_GUNICORN": TestShell.CHANGE_URL_TO_GUNICORN,

        "FROM": TestShell.FROM,
        "GET_JSON": TestShell.GET_JSON,
        "GET_HEADERS": TestShell.GET_HEADERS,
        "GET_TOKEN": TestShell.GET_TOKEN,
        "CLEAR": TestShell.CLEAR,
        "SET_VALUE": TestShell.SET_VALUE,
        "REMOVE_VALUE": TestShell.REMOVE_VALUE,
        "GET_RESPONSE": TestShell.GET_RESPONSE,
        "GET_RESPONSE_CODE": TestShell.GET_RESPONSE_CODE,
        "GET_RESPONSE_HEADERS": TestShell.GET_RESPONSE_HEADERS,
        "GET_RESPONSE_JSON": TestShell.GET_RESPONSE_JSON,
        "GET_RESPONSE_TEXT": TestShell.GET_RESPONSE_TEXT,
        "GET_RESPONSE_VALUE": TestShell.GET_RESPONSE_VALUE,
        "GET_RESPONSE_WITH": TestShell.GET_RESPONSE_WITH,  # old

        "ASSERT_CODE": TestShell.ASSERT_CODE,
        "ASSERT_VALUE": TestShell.ASSERT_VALUE,

        "AUTH": TestShell.AUTH,
        "AUTH_FROM": TestShell.AUTH_FROM,
        "GET": TestShell.GET,
        "POST": TestShell.POST,
        "PUT": TestShell.PUT,
        "DELETE": TestShell.DELETE,
    }

    for args in prompts:
        command = args[0]
        if command in commands:
            ret = commands[command](*args[1:])
            if ret:
                if isinstance(ret, dict):
                    for key in ret:
                        print(f"  - {CYAN}{key}{RESET}: {ret[key]}")
                else:
                    print(ret)
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
            print(f"  {RED}!{RESET} {e}{RESET}")


if __name__ == "__main__":
    main()
