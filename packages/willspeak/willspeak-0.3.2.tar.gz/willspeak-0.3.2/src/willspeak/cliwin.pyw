# Standard lib
import sys

# Local
from willspeak.cli import parser
from willspeak.utils import graceful_exception


@graceful_exception
def server() -> int:
    # We use argparse commands to select the function to call
    args = parser.parse_args(["server"] + sys.argv[2:])
    return args.func(args)
