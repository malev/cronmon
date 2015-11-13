import argparse
import datetime
import errno
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


def mkdir_p(path):
    """ 'mkdir -p' in Python """
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def store(content, *args, **kwargs):
    name = kwargs.get('name', 'default')
    output_dir = os.path.join(kwargs['location'], name)
    mkdir_p(output_dir)
    logfilename = str(int(time.time())) + '.json'
    with open(os.path.join(output_dir, logfilename), 'w') as logfile:
        logfile.write(content)


def execute(command, **kwargs):
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    start = time.time()
    stdout, stderr = process.communicate()
    end = time.time()
    status = process.returncode
    store(json.dumps({
        'status': status,
        'content': stdout,
        'error': stderr,
        'elapsed_time': int(end - start),
        'created_at': datetime.datetime.today().strftime("%Y-%m-%d-%H-%M")
    }), **kwargs)


def start(args):
    if not sys.stdin.isatty():
        store(sys.stdin.read(), name=args.name, location=args.location)
    else:
        execute(args.command, name=args.name, location=args.location)


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
        default='default',
        help='Name of the crontask to monitor'
    )
    parser.add_argument(
        '-c',
        '--command',
        action='store',
        help='Command to execute'
    )
    parser.add_argument(
        '-l',
        '--location',
        action='store',
        required=True,
        help="Directory where logfiles will be store"
    )
    args = parser.parse_args()
    start(args)
