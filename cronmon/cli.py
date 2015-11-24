import click
import run as crun
import log as clog
import server as cserver


@click.group()
def cli():
    """
    CronMon helps you monitor your cron tasks. Helps you handle the logging
    and provides you a callback to know when something is wrong. It also
    has a small webserver to help you navigate your logs.

    Examples:\n
        cronmon -c your-script.sh

        cronmon -c your-script.sh -n your-project -f fail-script.sh

        cronmon --config config.yml
    """
    pass


@cli.command()
@click.option('-c', '--command', help='Command to execute', required=False, default=None)
@click.option(
    '-l', '--location', help='location where logfiles will be store', required=False, default=None)
@click.option('-f', '--on-fail', help='When failing run', required=False, default=None)
@click.option('--config', help='Configuration file', required=False, default=None)
@click.option('-n', '--name', required=False, default='default')
def run(command, location, on_fail, config, name):
    crun.start(
        command=command,
        location=location,
        on_fail=on_fail,
        config=config,
        name=name
    )


@cli.command()
@click.option('-n', '--number', help='Number of log to show', required=False, default=None)
@click.option(
    '-l', '--location', help='Directory where logfiles will be store',
    required=False, default="~/cronmon")
@click.argument('name')
def log(number, name):
    clog.start(name, number)


@cli.command()
@click.option('-p', '--port', help='Port number', required=False, default=5000)
@click.option('-l', '--location', help='Directory where logfiles are stored', required=True)
def server(port, location):
    cserver.start(port, location)


def main():
    cli()


if __name__ == '__main__':
    print(__doc__)
