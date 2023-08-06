# Standard lib
from threading import Thread
from typing import Iterator
from io import BytesIO
import audioop
import queue

# Third party
import pyaudio

# Local
from willspeak import settings, inactive_flag


class SpeakerBase(Thread):
    """
    Base class for all audio speakers.
    """

    def __init__(self, *args, **kwargs):
        super(SpeakerBase, self).__init__(*args, **kwargs)
        self.queue = queue.Queue()

    def stop(self):
        """
        Stop current playback and clear any unprocessed chunks.
        """
        # Clear the queue of audio chunks
        with self.queue.mutex:
            self.queue.queue.clear()

    def play(self, audio_data: bytes):
        """
        Split audio data into chunks and add to processing queue.
        """
        audio_obj = BytesIO(audio_data)
        while dataframe := audio_obj.read(settings.chunk):
            self.queue.put(dataframe)

    def play_chunk(self, audio_chunk: bytes):
        """
        Take an audio chunk and add to processing queue.
        """
        self.queue.put(audio_chunk)

    def play_iterator(self, audio_stream: Iterator[bytes]):
        """
        Take an iterator of audio chunks and add them to processing queue.
        """
        for audio_chunk in audio_stream:
            self.queue.put(audio_chunk)

    def close(self):
        """Close any opened audio streams."""
        raise NotImplementedError()

    def _play_stream(self, audio_data: bytes):
        """Internal method that will play the given audio stream."""
        raise NotImplementedError()

    def run(self) -> None:
        """Continuously wait for and process any audio data."""
        try:
            while not inactive_flag.is_set():
                try:
                    audio_data = self.queue.get(timeout=settings.timeout)
                except queue.Empty:
                    continue

                try:
                    self._play_stream(audio_data)
                finally:
                    self.queue.task_done()
        finally:
            self.close()


class WaveSpeaker(SpeakerBase):
    """Speaker thread to handle processing of wave audio streams."""
    def __init__(self, *args, **kwargs):
        super(WaveSpeaker, self).__init__(*args, **kwargs)
        self._pyaudio = pyaudio.PyAudio()
        self._stream = self._create_stream()

    def _create_stream(self) -> pyaudio.Stream:
        """Create a pyaudio stream in stereo."""
        return self._pyaudio.open(format=pyaudio.paInt16, channels=2, rate=48000, output=True)

    def _play_stream(self, audio_data: bytes):
        # Convert audio chunk from mono to stereo before playing
        audio_data = audioop.tostereo(audio_data, 2, 1, 1)
        self._stream.write(audio_data)

    def close(self):
        # Close the audio stream
        self.stop()
        self._stream.close()
        self._pyaudio.terminate()
