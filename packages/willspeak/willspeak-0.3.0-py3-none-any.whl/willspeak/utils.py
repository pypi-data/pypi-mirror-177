# Standard lib
import functools
import typing

# Local
from willspeak import inactive_flag


def graceful_exception(func):
    """
    Decorator function to handle exceptions gracefully.
    And signal any threads to end.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> int:
        try:
            ret = func(*args, **kwargs)
        except KeyboardInterrupt:
            return 143
        else:
            # Return 0 if no return code was returned
            return ret if ret is not None else 0
        finally:
            inactive_flag.set()
    return wrapper


def ensure_int_range(min_value: int, max_value: int) -> typing.Callable[[str], int]:
    """
    Function that converts a string into an integer while ensuring the value is within the given range.

    :param min_value: The minimum allowed value.
    :param max_value: The maximum allowed value.
    """
    def wrapper(string: str) -> int:
        value = int(string)
        if min_value <= value <= max_value:
            return value
        else:
            raise ValueError(f"'{value}' is outside range, must be anywhere from {min_value} and {max_value}")

    return wrapper
