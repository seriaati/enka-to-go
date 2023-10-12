class EnkaAPIException(Exception):
    def __str__(self):
        return "Unknown error"


class WrongUIDFormat(EnkaAPIException):
    def __str__(self):
        return "UID must be a string of 9 digits"


class PlayerDoesNotExist(EnkaAPIException):
    def __str__(self):
        return "Player does not exist"


class GameMaintenance(EnkaAPIException):
    def __str__(self):
        return "Game is under maintenance"


class RateLimited(EnkaAPIException):
    def __str__(self):
        return "Rate limited"


class GeneralServerError(EnkaAPIException):
    def __str__(self):
        return "General server error"


class AlgoScrewedUpMassively(EnkaAPIException):
    def __str__(self):
        return "Algo screwed up massively"


def raise_for_retcode(retcode: int) -> None:
    if retcode == 400:
        raise WrongUIDFormat
    elif retcode == 404:
        raise PlayerDoesNotExist
    elif retcode == 424:
        raise GameMaintenance
    elif retcode == 429:
        raise RateLimited
    elif retcode == 500:
        raise GeneralServerError
    elif retcode == 503:
        raise AlgoScrewedUpMassively
    else:
        raise EnkaAPIException
