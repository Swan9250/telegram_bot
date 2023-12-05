from enum import IntEnum, auto


class GreetingConversation(IntEnum):
    NEED_FORM_PASS = auto()
    GET_NAME = auto()
    GET_SURNAME = auto()
    GET_LAST_NAME = auto()  # отчество
    GET_BIRTH_DATE = auto()
    GET_BIRTH_CITY = auto()
    GET_EYES_COLOR = auto()
    GET_HAIR_COLOR = auto()
    GET_FAVORITE_FLOWER = auto()
    GET_FAVORITE_PET = auto()
    GET_FAVORITE_BOOK = auto()
    GET_FAVORITE_FILM = auto()
    GET_FAVORITE_SONG = auto()
    GET_HOBBIES = auto()
    GET_FAVORITE_SEASON = auto()
    GET_BEST_QUALITY = auto()
    GET_WORST_QUALITY = auto()
    GET_WORK = auto()
    GET_FAVORITE_MEAL = auto()
    GET_SALARY = auto()
