import datetime
import errno
import json
import os
import subprocess
import time

import yaml

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
        'success': check_success(status),
        'status': status,
        'content': stdout,
        'error': stderr,
        'elapsed_time': int(end - start),
        'created_at': datetime.datetime.today().strftime("%Y-%m-%d-%H-%M")
    }), **kwargs)
    return status == 0


def check_success(status):
    return int(status) == 0


class Config(object):
    '''
    Returns configuration whether are coming from
    arguments on command line or the configuration
    file
    '''
    def __init__(self, **config):
        self._command = config.get('command')
        self._location = config.get('location', '~')
        self._on_fail = config.get('on_fail')
        self._name = config.get('name')
        if self._name is None:
            self._name = 'default'
        self.config = {}
        config_file = config.get('config')
        if config_file is not None:
            with open(config_file) as cfile:
                self.config = yaml.load(cfile.read())

    @property
    def command(self):
        return self.config.get('command', self._command)

    @property
    def location(self):
        return self.config.get('location', self._location)

    @property
    def on_fail(self):
        return self.config.get('on_fail', self._on_fail)

    @property
    def name(self):
        return self.config.get('name', self._name)

    def has_on_fail(self):
        return self.on_fail is not None


def start(**kwargs):
    c = Config(**kwargs)

    if not execute(c.command, name=c.name, location=c.location):
        if c.has_on_fail():
            subprocess.call(c.on_fail)


if __name__ == '__main__':
    print(__doc__)
