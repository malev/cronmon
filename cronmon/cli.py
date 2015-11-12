import argparse
import datetime
import json
import os
import subprocess
import sys
import time

description = """
Monitor and log your crontasks
"""

example = """
examples:
    your-script.sh arguments | cronmon -n your-project
    conrmon -n your-project -c "your-script.sh arguments"
"""


def store(content, **kwargs):
    output = kwargs.get('output', '~/cronmon')
    name = kwargs.get('name', 'default')
    logfilename = str(int(time.time())) + '.json'
    with(os.path.join(output, name, logfilename)) as logfile:
        logfile.write(content)


def execute(command, **kwargs):
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    stdout, stderr = process.communicate()
    status = process.returncode
    store(json.dumps({
        'status': status,
        'content': stdout.read(),
        'error': stderr.read(),
        'created_at': datetime.datetime.today().strftime("%Y-%m-%d-%H-%M")
    }), **kwargs)


def start(args):
    if not sys.stdin.isatty():
        store(sys.stdin.read(), name=args.name, output=args.output)
    else:
        store(execute(args.command), name=args.name, output=args.output)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description,
        epilog=example,
        add_help=True
    )
    parser.add_argument(
        '-n',
        '--name',
        action='store',
        default=None,
        help='Name of the crontask to monitor'
    )
    parser.add_argument(
        '-c',
        '--command',
        action='store',
        help='Command to execute'
    )
    parser.add_argument(
        '-o',
        '--output',
        action='store',
        default='~/cronmon',
        help="Directory where logfiles will be store"
    )
    args = parser.parse_args()
    start(args)
