"""
This module contains filter functions that should filter out and/or manipulate the text it's processing.

There are 3 different types of filters.
    * Decider: Function that checks if given text should be processed or not. Returning None if not.
    * Filter: Simple function that takes a given text and filters out any unwanted text before returning it.
    * Processor: This function takes a given text and splits it up into more manageable parts. Faster when
                 dealing with larger chunks of text.
"""

# Standard lib
from typing import Callable
import re

T_FILTER_RTN = str | list[str] | None
T_FILTER_CALL = Callable[[str], T_FILTER_RTN]
text_filters: list[T_FILTER_CALL] = []
regex_cache = {}


def process_text(text: str) -> list[str]:
    """Run all filters & processers on given text string."""
    text_list = [text]
    for func in text_filters:
        new_list = []
        for text in text_list:
            ret = func(text)
            if isinstance(text, list):
                new_list.extend(ret)
            elif text:
                new_list.append(ret)

        text_list = new_list

    return text_list


def re_cache(regex: str):
    """Takes regex string, compile it, and cache it for later use."""
    if regex in regex_cache:
        return regex_cache[regex]
    else:
        compiled = re.compile(regex)
        regex_cache[regex] = compiled
        return compiled


def text_filter(func) -> T_FILTER_CALL:
    """
    Function decorator to register a text filter.

    A text filter takes a string and strips out unwanted text patterns.
    """
    def wrapper(text):
        try:
            return func(text)
        except Exception as e:
            print("ERROR:", e)
            return text

    text_filters.append(wrapper)
    return wrapper


# Deciders
################################################################################

@text_filter
def ignore_only_url(text: str) -> str | None:
    """If the given text only contains an url then ignore it."""
    re_filter = re_cache(r"^(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])$")
    # Returns text only if match is not found
    if not re.match(re_filter, text):
        return text


# Filters
################################################################################

@text_filter
def filter_read_more_at(text: str) -> str:
    """
    Strip out any 'Read more at.' text that a lot
    of sites like to add when any text is copied.
    """
    re_filter = re_cache(r"([Rr]ead more\s*[at]*:*\s+http\S+|[Ss]ee more at:*\s+http\S+)")
    return re.sub(re_filter, "", text).strip()


# Processors
################################################################################
