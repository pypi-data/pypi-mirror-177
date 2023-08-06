# Standard lib
from dataclasses import dataclass, field, fields
import typing


@dataclass(eq=False, frozen=True)
class Voice(object):
	"""
	Voice dataclass.

	:ivar id: ID of the voice.
	:ivar name: The voice name.
	:ivar lang: The language of the voice, including the region, (United States) or (Great Britain).
	:ivar gender: The gender, male or female.
	:ivar age: The age group of the vocie. e.g. Adult, child.
	"""

	id: int | str
	name: str
	lang: str = field(kw_only=True, default="")
	gender: str = field(kw_only=True, default="")
	age: str = field(kw_only=True, default="")
	token: typing.Any = field(kw_only=True, default=None, repr=False)

	def asdict_shallow(self) -> dict:
		"""Converts the dataclass obj to a dict using a shallow copy only."""
		# We do not want the token variable to be return, token is internal
		return dict((_field.name, getattr(self, _field.name)) for _field in fields(self) if _field.name != "token")
