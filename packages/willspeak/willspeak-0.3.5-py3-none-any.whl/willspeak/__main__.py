# Standard lib
import argparse
import sys

# Local
from willspeak import settings, scripts
from willspeak.utils import graceful_exception, ensure_int_range


def tts_client_settings(sub_parsser):
    """
    Add volume & rate to arg parser.
    """
    # Add volume setting
    sub_parsser.add_argument(
        "--volume",
        help="Set the tts volume. Value can be anyting from 0 to 100",
        default=settings.volume,
        type=ensure_int_range(0, 100),
    )
    # Add speaking rate setting
    sub_parsser.add_argument(
        "--rate",
        help="Set the tts speaking rate. Value can be anyting from 1 to 10",
        default=settings.rate,
        type=ensure_int_range(-10, 10),
    )
    # Add voice setting
    sub_parsser.add_argument(
        "--voice",
        help="Set the tts voice using a voice id.",
        default=None,
    )


# CLI Arguments
parser = argparse.ArgumentParser(prog=settings.appname)
subcommands = parser.add_subparsers(title="commands", required=True, dest="cmd")
parser.add_argument(
    "-e", "--engine",
    default="sapi5",
    choices=["sapi5"],
    help="Text to speach engine to use. Default('sapi5')"
)

# Server Command
sub = subcommands.add_parser("server", help=f"Run {settings.appname} in server mode")
sub.set_defaults(func=scripts.server)
sub.add_argument(
    "--bind_addr",
    help=f"The IP interface to bind to, default is 0.0.0.0 (all addresses).",
    metavar="",
    default="0.0.0.0",
)
sub.add_argument(
    "--bind_port",
    help="The port number to listen on.",
    metavar="",
    default=settings.port,
    type=int,
)

# Client Command
sub = subcommands.add_parser("client", help=f"Run {settings.appname} in server mode")
sub.set_defaults(func=scripts.client)
tts_client_settings(sub)
sub.add_argument(
    "--addr",
    help=f"The IP/Hostname of the {settings.appname} server.",
    metavar="",
    required=True,
)
sub.add_argument(
    "--port",
    help="The port number to connect to on the server.",
    metavar="",
    default=settings.port,
    type=int,
)

# Local Command
sub = subcommands.add_parser("local", help=f"Run {settings.appname} in local mode")
sub.set_defaults(func=scripts.local)
tts_client_settings(sub)

# Stop Command
sub = subcommands.add_parser("stop", help="Stop current speach and clear any queue")
sub.set_defaults(func=scripts.stop)


@graceful_exception
def entrypoint() -> int:
    args = parser.parse_args(sys.argv[1:] or ["-h"])
    return args.func(args)


@graceful_exception
def run_server() -> int:
    args = parser.parse_args(["server"] + sys.argv[2:])
    return args.func(args)


@graceful_exception
def run_client() -> int:
    args = parser.parse_args(["client"] + sys.argv[2:])
    return args.func(args)


@graceful_exception
def run_local() -> int:
    args = parser.parse_args(["local"] + sys.argv[2:])
    return args.func(args)


@graceful_exception
def run_stop() -> int:
    args = parser.parse_args(["stop"] + sys.argv[2:])
    return args.func(args)


# This is only used for manual testing
if __name__ == "__main__":
    exit_code = entrypoint()
    sys.exit(exit_code)
