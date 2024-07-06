#!/usr/bin/python3

'''
    Shell for manual testing.
    Uses similar testing commands used in scripts.

    Help for commands in shell_help.txt. You can also run the HELP command.
'''

from pathlib import Path
from random import randint
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


    amenity_ids: list[str] = []
    host_id: str | None = None
    city_id: str | None = None

    place: dict | None = None

    @classmethod
    def CREATE_CITY(cls, num: int) -> str:
        '''
            Creates city to create place.
        '''

        if isinstance(num, str):
            num = int(num)

        cls.FROM(f"cities/valid_city_{num}.json")
        cls.POST("/cities")
        cls.ASSERT_CODE(201)
        city_id = cls.GET_RESPONSE_VALUE("id")
        cls.city_id = city_id
        return city_id

    @classmethod
    def CREATE_USER(cls, num: int) -> str:
        '''
            Creates user to host place.
        '''

        if isinstance(num, str):
            num = int(num)

        cls.FROM(f"users/valid_user_{num}.json")
        cls.POST("/users")
        cls.ASSERT_CODE(201)
        user_id = cls.GET_RESPONSE_VALUE("id")
        cls.host_id = user_id
        return user_id

    @classmethod
    def CREATE_AMENITY(cls, num: int) -> str:
        '''
            Creates amenity to create place.
        '''

        if isinstance(num, str):
            num = int(num)

        cls.FROM(f"amenities/valid_amenity_{num}.json")
        cls.POST("/amenities")
        cls.ASSERT_CODE(201)
        return cls.GET_RESPONSE_VALUE("id")

    @classmethod
    def CREATE_AMENITIES(
            cls,
            number_of_amenities: int | None = None
        ) -> list[str]:
        '''
            Creates multiple amenities and returns a list of their ids.
        '''

        # Shellization
        if isinstance(number_of_amenities, str):
            number_of_amenities = int(number_of_amenities)

        if number_of_amenities is None:
            number_of_amenities = randint(0, 5)
        amenity_ids = []

        available = [i for i in range(1, 6)]
        for _ in range(1, number_of_amenities + 1):
            if len(available) == 0:
                break
            index = randint(0, len(available) - 1)
            num = available.pop(index)
            amenity_id = cls.CREATE_AMENITY(num)
            amenity_ids.append(amenity_id)

        cls.amenity_ids = amenity_ids
        return amenity_ids

    @classmethod
    def CREATE_PLACE(
        cls,
        num: int,
        number_of_amenities: int | None = None,
    ) -> dict:
        '''
            Creates a place:
                -> Creates all the necessary objects to create a place.
                -> Creates place using POST.
                -> GETs all places.
                -> Takes created place via name.
                -> Asserts that attributes were assigned successfully.
                -> Returns place w/o created_at or updated_at
        '''

        # Shellization
        if isinstance(num, str):
            num = int(num)
        if isinstance(number_of_amenities, str):
            number_of_amenities = int(number_of_amenities)

        # Create external objects
        host_id = cls.CREATE_USER(num)
        city_id = cls.CREATE_CITY(num)
        amenity_ids = cls.CREATE_AMENITIES(number_of_amenities)

        # Take dict from json number num
        cls.FROM(f"places/valid_place_{num}.json")

        # Assign ids to place json
        cls.SET_VALUE("host_id", host_id)
        cls.SET_VALUE("city_id", city_id)
        cls.SET_VALUE("amenity_ids", amenity_ids)

        # POST Place
        cls.POST("/places")

        # If not 201 delete other objects
        if cls.last_response.status_code != 201:
            cls.DELETE_PLACE(
                host_id=host_id,
                city_id=city_id,
                amenity_ids=amenity_ids
            )

        # Copy response
        place = cls.json.copy()
        place["amenity_ids"] = amenity_ids.copy()  # Deep copy
        place["id"] = cls.GET_RESPONSE_VALUE("id")
        cls.place = place
        cls.amenity_ids = amenity_ids
        cls.host_id = host_id
        cls.city_id = city_id

        return place

    @classmethod
    def DELETE_PLACE(
        cls,
        place_id: str | None = None,
        host_id: str | None = None,
        city_id: str | None = None,
        amenity_ids: list[str] | None = None,
        **kwargs
    ) -> None:
        '''
            Deletes a place using either args or class attributes.
        '''
        if place_id is None:
            if cls.place is not None:
                place_id = cls.place.get("id")
        if place_id is not None:
            cls.DELETE(f"/users/{host_id}")
            cls.ASSERT_CODE(204)
            cls.place = None
        if host_id is None:
            if cls.host_id is not None:
                host_id = cls.host_id
        if host_id is not None:
            cls.DELETE(f"/users/{host_id}")
            cls.ASSERT_CODE(204)
            cls.host_id = None
        if city_id is None:
            if cls.city_id is not None:
                city_id = cls.city_id
        if city_id is not None:
            cls.DELETE(f"/cities/{city_id}")
            cls.ASSERT_CODE(204)
            cls.city_id = None
        if amenity_ids is None:
            if cls.amenity_ids is not None:
                amenity_ids = cls.amenity_ids
        if amenity_ids is not None:
            for amenity_id in amenity_ids:
                cls.DELETE(f"/amenities/{amenity_id}")
                cls.ASSERT_CODE(204)
            cls.amenity_ids = None


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
        if len(args) >= 2:
            for i, arg in enumerate(args[1:]):
                if arg[0] == "[":
                    arg = arg.replace("[", "")
                    arg = arg.replace("]", "")
                    args[i] = list(arg.split(","))
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
