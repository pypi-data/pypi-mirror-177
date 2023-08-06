import subprocess
import click

def run_command(command_list):
    try:
        process = subprocess.Popen(
            command_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        result = process.communicate()
        if process.returncode == 0:
            return process.returncode
        else:
            click.echo(click.style('There was an error running your command.', fg='red'))
            click.echo(click.style(f'{result}', fg='red'))
            return process.returncode
    except subprocess.CalledProcessError as ex:
        click.echo(click.style('There was an error running your command.', fg='red'))
        click.echo(click.style(f'{ex}', fg='red'))
        return 1

