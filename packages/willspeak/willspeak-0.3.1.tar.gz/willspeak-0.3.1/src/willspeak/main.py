# Local
from .monitors import ClipboardMonitor, ProcessMonitor
from .utils import graceful_exception
from .audio import WaveSpeaker


@graceful_exception
def stop(_):
    """Send a stop command to running process."""
    process_pipe = ProcessMonitor()
    process_pipe.send_stop()
    return 0


@graceful_exception
def server(args):
    """Set up the TTS engine in server mode."""
    from .tts.sapi5 import server as sapiserver
    sapiserver.start(args.bind_addr, args.bind_port)


@graceful_exception
def client(args):
    """Set up the TTS engine in client mode. Requires a running tts server."""
    from willspeak.tts.sapi5.client import TTSClient
    return speaking_mode(TTSClient, args, addr=args.addr, port=args.port)


@graceful_exception
def local(args):
    """Set up the TTS engine in local mode."""
    from willspeak.tts.sapi5.local import TTSClient
    return speaking_mode(TTSClient, args)


def speaking_mode(tts_engine, args, **init_args):
    """Run the tts engine, monitor clipboard and speak any text."""
    # Welcome the user
    tts = tts_engine(**init_args)
    tts.volume = args.volume
    tts.rate = args.rate

    # Welcome user
    tts.speak("Welcome to the new will speak!")

    # Allow for process communication to control current state
    process_pipe = ProcessMonitor()
    process_pipe.start_server(stop=tts.stop)

    # Monitor clipboard for text to speak
    monitor = ClipboardMonitor()
    monitor.wait_for_text(tts.speak)
    return 0
