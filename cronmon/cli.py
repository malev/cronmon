import click
import run as crun
import server as cserver


@click.group()
def cli():
    """
    CronMon helps you monitor your cron tasks. Helps you handle the logging
    and provides you a callback to know when something is wrong. It also
    has a small webserver to help you navigate your logs.

    Examples:\n
      cronmon run -c your-script.sh\n
      cronmon run --config config.yml\n
      cronmon serve -l ~/cronmon
    """
    pass


@cli.command()
@click.option('-c', '--command', help='Command to execute', required=False, default=None)
@click.option(
    '-l', '--location', help='location where logfiles will be store', required=False)
@click.option('-f', '--on-fail', help='When failing run', required=False, default=None)
@click.option('-s', '--on-success', help='When succeeding run', required=False, default=None)
@click.option('--config', help='Configuration file', required=False, default=None)
@click.option('-n', '--name', required=False, default='default')
def run(command, location, on_fail, on_success, config, name):
    crun.start(
        command=command,
        location=location,
        on_fail=on_fail,
        on_success=on_success,
        config=config,
        name=name
    )


@cli.command()
@click.option('-p', '--port', help='Port number', required=False, default=5000)
@click.option('-l', '--location', help='Directory where logfiles are stored', required=True)
def server(port, location):
    cserver.start(port, location)


def main():
    cli()


if __name__ == '__main__':
    print(__doc__)
