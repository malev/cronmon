import datetime
import errno
import json
import os
import subprocess
import sys
import time

"""
Run and store the output
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


def start(command, location, name):
    if not sys.stdin.isatty():
        store(sys.stdin.read(), name=name, location=location)
    else:
        execute(command, name=name, location=location)


if __name__ == '__main__':
    print(__doc__)