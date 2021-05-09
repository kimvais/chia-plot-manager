import click
from plotmanager.library.utilities.commands import (
    analyze_logs as _analyze_logs,
    start_manager,
    stop_manager,
    view as _view,
    )
from plotmanager.library.utilities.exceptions import InvalidArgumentException

help_description = '''
There are a few different actions that you can use: "start", "restart", "stop", "view", and "analyze_logs". "start" will 
start a manager process. If one already exists, it will display an error message. "restart" will try to kill any 
existing manager and start a new one. "stop" will terminate the manager, but all existing plots will be completed. 
"view" can be used to display an updating table that will show the progress of your plots. Once a manager has started it 
will always be running in the background unless an error occurs. This field is case-sensitive.

"analyze_logs" is a helper command that will scan all the logs in your log_directory to get your custom settings for
the progress settings in the YAML file.
'''


@click.group()
def cli():
    pass


@cli.command()
def start():
    start_manager()


@cli.command()
def restart():
    stop_manager()
    start_manager()


@cli.command()
def stop():
    stop_manager()


@cli.command()
def view():
    _view()


@cli.command()
def analyze_logs():
    _analyze_logs()
