""" Entrypoint of the CLI """
import click
from datetime import datetime

from src.commands import authorize, polling, loadcsv, onfleettasks


@click.group()
def cli():
    pass


@cli.command()
@click.argument("name")
@click.option("--check", is_flag=True, default=False, help="Check the current API key.")
@click.option("-k", "--key", default=None, help="Update API keys key.", type=str)
def auth(name: str, key: str, check: bool):
    """
    Check your Azure Onfleet Function App API Key or add a new API key.
    KEY NAMES: ONFLEET_DEV, AZURE_ADMIN, GOOGLE_GEOCODING

    $ supersod auth <NAME> -k <API_KEY>

    $ supersod auth <NAME> --check
    """
    authorize.auth(name, key, check)


@cli.command()
@click.argument("filetype")
@click.option("-f", "--filepath", default='./tasks.csv', help="Filepath of tasks file.", type=click.Path(exists=True))
def load(filetype: str, filepath: str):
    """
    Load a task file into Onfleet.

    $ supersod load csv

    $ supersod load csv -f '/home/users/exampleuser/downloads/Rev02_22Nov2022.csv'
    """
    loader = loadcsv.Loader()
    if filetype == 'csv':
        tasks_list, num_tasks = loader.load_csv(filepath)
        _tasks = loader.make_tasks(tasks_list)
        with click.progressbar(_tasks, length=num_tasks) as bar:
            for _ in bar:
                bar.update(1)


@cli.command()
@click.argument("action")
@click.option("-f", "--from", "days_from", default=3, help="Days from.", type=int)
@click.option("-t", "--to", "days_to", default=90, help="Days to.", type=int)
@click.option("--v", "verbose", is_flag=True, show_default=True, default=False, help="Verbose - print entire payload.")
def tasks(action: str, days_from: int, days_to: int, verbose: bool):
    """
    List or clear tasks in Onfleet.

    $ supersod tasks list

    $ supersod tasks clear --from 7
    """
    oft = onfleettasks.OnfleetTasks()
    if action == 'list':
        task_list = oft.get_tasks(days_from, days_to)
        for task in task_list:
            time_created = datetime.fromtimestamp(task["timeCreated"]/1000).strftime("%Y-%m-%d %H:%M:%S")
            if not verbose:
                click.secho(f'{task["id"]} | {task["destination"]["address"]["city"]} @ {time_created}')
            else:
                print(task)
        click.secho(f"Retrieved {len(task_list)} tasks", fg='green')

    if action == 'clear':
        oft.clear_tasks(days_from, days_to)
