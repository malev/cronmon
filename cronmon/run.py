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


def execute(config):
    process = subprocess.Popen(
        config.command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    start = time.time()
    stdout, stderr = process.communicate()
    end = time.time()
    status = process.returncode
    try:
        content = json.loads(stdout)
    except ValueError:
        content = stdout

    Storer(config).store(json.dumps({
        'success': check_success(status),
        'status': status,
        'content': content,
        'error': stderr,
        'elapsed_time': int(end - start),
        'created_at': datetime.datetime.today().strftime("%Y-%m-%d-%H-%M")
    }))
    return status == 0


def check_success(status):
    return int(status) == 0


class Storer(object):
    def __init__(self, config):
        self.config = config

    def store(self, content):
        if self.config.one_file:
            self.append(content)
        else:
            self.log(content)

    def append(self, content):
        append_file = self.config.name + '.log'
        mkdir_p(self.config.location)
        with open(os.path.join(self.config.location, append_file), 'a') as logfile:
            logfile.write(content + '\n')

    def log(self, content):
        logfilename = str(int(time.time())) + '.json'
        output_dir = os.path.join(self.config.location, self.config.name)
        mkdir_p(output_dir)
        with open(os.path.join(output_dir, logfilename), 'w') as logfile:
            logfile.write(content)


class Config(object):
    '''
    Returns configuration whether are coming from
    arguments on command line or the configuration
    file
    '''
    def __init__(self, **config):
        self._command = config.get('command')
        self._location = config.get('location')
        if config.get('location') is None:
            self._location = os.path.expanduser('~')
        self._one_file = config.get('one_file', False)
        self._on_fail = config.get('on_fail')
        self._on_success = config.get('on_success')
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
    def on_success(self):
        return self.config.get('on_success', self._on_success)

    @property
    def one_file(self):
        return self.config.get('one_file', self._one_file)

    @property
    def name(self):
        return self.config.get('name', self._name)

    def has_on_fail(self):
        return self.on_fail is not None

    def has_on_success(self):
        return self.on_success is not None


def start(**kwargs):
    c = Config(**kwargs)

    if not execute(c):
        if c.has_on_fail():
            subprocess.call(c.on_fail)
    elif c.has_on_success():
        subprocess.call(c.on_success)


if __name__ == '__main__':
    print(__doc__)
