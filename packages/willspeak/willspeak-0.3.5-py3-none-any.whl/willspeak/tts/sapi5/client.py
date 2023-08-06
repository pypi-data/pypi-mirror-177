# Third party
import requests

# Local
from ..voice import Voice
from ...audio import WaveSpeaker


class TTSClient(object):
	"""
	TTS driver module to control microsoft SAPI TTS Engine.
	"""

	# Methods
	GET = "GET"
	PUT = "PUT"
	POST = "POST"

	# Endpoints
	EPT_SETTINGS = "/settings"
	EPT_VOICES = "/voices"
	EPT_SPEAK = "/speak"
	EPT_STOP = "/stop"

	speaker_class = WaveSpeaker

	def __init__(self, addr: str, port: int):
		self.base_url = f"http://{addr}:{port}"
		self.speaker = self.speaker_class()
		self.speaker.start()

		# Requests
		self.session = requests.Session()

	def _make_json_request(self, method: str, url: str, **kwargs):
		url = self.base_url + url
		resp = self.session.request(method, url, **kwargs)
		resp.raise_for_status()
		resp_datta = resp.json()
		resp.close()
		return resp_datta

	def get_voices(self) -> list[Voice]:
		"""
		Return list of avalable voices as a Voice object.
		"""
		voices = []
		for voice in self._make_json_request(self.GET, self.EPT_VOICES):
			del voice["url"]
			voice_obj = Voice(**voice)
			voices.append(voice_obj)

		return voices

	@property
	def voice(self) -> Voice:
		"""
		Return the current selected voice as a Voice object.
		"""
		resp = self._make_json_request(self.GET, self.EPT_SETTINGS)
		del resp["voice"]["url"]
		return Voice(**resp["voice"])

	@voice.setter
	def voice(self, voice: Voice | int | str):
		"""
		Change voice to selected voice.

		Value can be a voice object, voice id (int) or voice name (str).
		"""
		if isinstance(voice, Voice):
			voice = voice.id

		req_data = {"voice": voice}
		self._make_json_request(self.PUT, self.EPT_SETTINGS, json=req_data)

	@property
	def rate(self) -> int:
		"""
		Return the current speech rate.
		"""
		resp = self._make_json_request(self.GET, self.EPT_SETTINGS)
		return resp["rate"]

	@rate.setter
	def rate(self, rate: int):
		"""
		Change the speach rate of the voice.

		value : integer --- Rate to set the voice to.

		Value must be between -10 to +10.
		"""
		req_data = {"rate": rate}
		self._make_json_request(self.PUT, self.EPT_SETTINGS, json=req_data)

	@property
	def volume(self) -> int:
		"""
		Return the current volume level.
		"""
		resp = self._make_json_request(self.GET, self.EPT_SETTINGS)
		return resp["volume"]

	@volume.setter
	def volume(self, volume: int):
		"""
		Chagne the volume of the voice.

		value : int --- level of the volume to change to.
		"""
		req_data = {"volume": volume}
		self._make_json_request(self.PUT, self.EPT_SETTINGS, json=req_data)

	def speak(self, text):
		"""
		Send text to tts engine and speak.
		"""
		raw_text = text.encode("utf8")
		url = self.base_url + self.EPT_SPEAK
		headers = {"content-type": "text/plain; charset=UTF-8", "content-length": str(len(raw_text))}
		resp = self.session.request(self.POST, url, data=raw_text, headers=headers, stream=True)
		resp.raise_for_status()

		# Stream the response into the speaker
		iterator = resp.iter_content(4096)
		self.speaker.play_iterator(iterator)
		resp.close()

	def stop(self):
		"""
		Stop current speak request.
		"""
		self._make_json_request(self.GET, self.EPT_STOP)

	def close(self):
		self.session.close()
