import click
from stochasticx.utils.preferences import Preferences, AppModes

@click.group(name="config")
def config_command():
    pass

@click.command(name="inspect")
def inspect_command():
    preferences = Preferences.load()
    click.secho("[+] You are in the **{}** mode...".format(preferences.current_mode), bold=True)


@click.command(name="local")
def local_command():
    click.secho("[+] Setting up **local** mode...", bold=True)
    preferences = Preferences.load()
    preferences.current_mode = AppModes.LOCAL
    Preferences.save(preferences)

@click.command(name="cloud")
def remote_command():
    click.secho("[+] Setting up **cloud** mode...", bold=True)
    preferences = Preferences.load()
    preferences.current_mode = AppModes.CLOUD
    Preferences.save(preferences)


config_command.add_command(inspect_command)
config_command.add_command(local_command)
config_command.add_command(remote_command)