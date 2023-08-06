# Standard lib
from typing import Callable
import hashlib

# Third party
# noinspection PyUnresolvedReferences
from comtypes.client import CreateObject

# Local
from ..voice import Voice
from ...audio import WaveSpeaker
from ... import settings

# Stream Formats
SAFT22kHz16BitMono = 22
SAFT22kHz16BitStereo = 23
SAFT24kHz16BitMono = 26
SAFT24kHz16BitStereo = 27
SAFT32kHz16BitMono = 30
SAFT32kHz16BitStereo = 31
SAFT44kHz16BitMono = 34
SAFT44kHz16BitStereo = 35
SAFT48kHz16BitMono = 38
SAFT48kHz16BitStereo = 39

# Speak Flags
SVSFDefault = 0
SVSFlagsAsync = 1
SVSFPurgeBeforeSpeak = 2
SVSFIsFilename = 4
SVSFIsXML = 8
SVSFIsNotXML = 16
SVSFPersistXML = 32


def create_voice_obj(cvoice) -> Voice:
	"""Takes a C SpObjectToken voice object converting to a python data object."""
	# The description contains both the name and lang
	# The real lang attribute is a number (strange)
	full_name = cvoice.GetDescription()
	name, lang = full_name.split(" - ", 1)
	name = name.replace("Desktop", "").replace("Mobile", "").strip()
	lang = lang.strip()

	# We create ID instead of using the available one
	# The available one is a mix of version and name with some other crap
	voice_id = int(str(int(hashlib.sha1(full_name.encode("utf8")).hexdigest(), 16))[:8])

	return Voice(
		id=voice_id,
		name=name,
		lang=lang,
		age=cvoice.GetAttribute("Age"),
		gender=cvoice.GetAttribute("Gender"),
		token=cvoice,
	)


class TTSClient(object):
	"""
	TTS driver module to control microsoft SAPI TTS Engine.
	"""

	speaker_class = WaveSpeaker

	def __init__(self, server_mode=False):
		self._engine = CreateObject("SAPI.SPVoice")
		if not server_mode:
			self._speaker = self.speaker_class()
			self._speaker.start()
		else:
			self._speaker = None

	# noinspection PyMethodMayBeStatic
	def create_memory_stream(self):
		"""
		Create SAPI in memory audio stream.
		"""
		stream = CreateObject("SAPI.SpMemoryStream")
		# Mono keeps the transfer size down
		# Audio stream can always be converted to stereo after the fact
		stream.Format.Type = SAFT48kHz16BitMono
		return stream

	def get_voices(self) -> list[Voice]:
		"""
		Return list of avalable voices as a Voice object.
		"""
		return [create_voice_obj(attr) for attr in self._engine.GetVoices()]

	@property
	def voice(self) -> Voice:
		"""
		Return the current selected voice as a Voice object.
		"""
		voice = self._engine.Voice
		return create_voice_obj(voice)

	@voice.setter
	def voice(self, value: Voice | int | str):
		"""
		Change voice to selected voice.

		Value can be a voice object, voice id (int) or voice name (str).
		"""
		if isinstance(value, Voice):
			self._engine.Voice = value.token
			return

		# Search for voice using given id or name
		for voice in self.get_voices():
			# Do the check as strings, as the voice ID can be a string
			if str(voice.id) == str(value) or voice.name == value:
				self._engine.Voice = voice.token
				break
		else:
			message = f"No voice found matching ID: {value}"
			raise ValueError(message)

	@property
	def rate(self) -> int:
		"""
		Return the current speech rate.
		"""
		return self._engine.Rate

	@rate.setter
	def rate(self, rate: int):
		"""
		Change the speach rate of the voice.

		value : integer --- Rate to set the voice to.

		Value must be between -10 to +10.
		"""
		if rate < -10 or rate > 10:
			raise ValueError("invalid rate %s" % rate)
		else:
			self._engine.Rate = rate

	@property
	def volume(self) -> int:
		"""
		Return the current volume level.
		"""
		return self._engine.Volume

	@volume.setter
	def volume(self, value: int):
		"""
		Chagne the volume of the voice.

		value : int --- level of the volume to change to.
		"""
		if value < 0 or value > 100:
			raise ValueError("invalid volume %s" % value)
		else:
			self._engine.Volume = value

	def speak(self, text: str):
		"""
		Send text to tts engine and speak.
		"""
		callback = self._speaker.play_chunk
		stream = self.create_memory_stream()
		self.raw_speak(stream, callback, text)

	def raw_speak(self, stream, callback: Callable[[bytes], None], text: str) -> bool:
		"""
		Call the speach engin and send all audio to the given stream.

		:returns bool: Returns True if command completed, False if command timed out.
		"""
		self._engine.AudioOutputStream = stream
		self._engine.Speak(text, SVSFlagsAsync)

		# Wait 10 seconds for the conversion to complete
		# Any longer than that and there must be an issue
		# WaitUntilDone returns False when it times out
		completed = not self._engine.WaitUntilDone(settings.speak_timeout)
		if completed:
			self.stop()
			self._engine.Speak("Error: Speak Request timed out")

		stream.Seek(0)
		while True:
			audio_chunk, data_size = stream.read(settings.chunk)
			if data_size:
				callback(bytes(audio_chunk))
			else:
				break

		return completed

	def stop(self):
		"""
		Stop current speak request.
		"""
		self._engine.Speak("", SVSFPurgeBeforeSpeak)
		if self._speaker is not None:
			self._speaker.stop()

	"""
	# May not need this, Just here for reference
	def speak_to_file(self, text, filepath):
		file_stream = CreateObject("SAPI.SPFileStream")
		file_stream.Format.Type = 39
		file_stream.Open(filepath, 3)
		self._engine.AudioOutputStream = file_stream
		self._engine.Speak(text)
		file_stream.Close()
		self._engine.AudioOutputStream = self._stream
	"""
