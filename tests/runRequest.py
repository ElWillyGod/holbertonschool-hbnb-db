
'''
    Shell for manual testing.
    Uses similar testing commands used in scripts.
'''

from testlib import HTTPTestClass
from os import argv
from tokenize import tokenize

class Tests(HTTPTestClass):
    '''
        Tests
    '''


def main() -> None:
    '''
        Interactive shell
    '''

    loop = True

    def exit() -> None:
        loop = False

    commands: dict[str: function] = {
        "exit": exit
    }

    while loop:
        prompt = input("$ ")
        if prompt in commands:
            prompt()


if __name__ == "__main__":
    main()
