from pathlib import Path

import click
import sys
import requests
from stochasticx.utils.preferences import Preferences, AppModes
from stochasticx.constants.urls import LocalRoutes
from stochasticx.datasets.datasets import Datasets, Dataset
from stochasticx.utils.parse_utils import print_table
from stochasticx.datasets.local_datasets import LocalDataset
from stochasticx.utils.auth_utils import AuthUtils
from stochasticx.utils.spinner_slash import Spinner


@click.group(name="datasets")
def datasets():
    try:
        AuthUtils.get_auth_headers()
    except:
        sys.exit()

    preferences = Preferences.load()

    if preferences.current_mode == AppModes.LOCAL:
        try:
            response = requests.get(LocalRoutes.HEALTH_REGISTRY)
            response.raise_for_status()
        except:
            click.secho("[+] Registry is not initilized. Run the command stochasticx local init", fg="red", bold=True)
            sys.exit(1)



@click.command(name="ls")
def ls_datasets():
    preferences = Preferences.load()

    if preferences.current_mode == AppModes.CLOUD:
        click.secho("\n[+] Collecting all datasets\n", fg='blue', bold=True)
    
        columns, values = Datasets.get_datasets(fmt="table")
        print_table(columns, values)
    else:
        click.secho("\n[+] Collecting all local datasets\n", fg='blue', bold=True)
        columns, values = Datasets.get_local_datasets()
        print_table(columns, values)


@click.command(name="inspect")
@click.option('--id', help='Dataset ID')
def dataset_inspect(dataset_id):
    preferences = Preferences.load()

    if preferences.current_mode == AppModes.CLOUD:
        click.secho("\n[+] Collecting information from the dataset\n", fg='blue', bold=True)
    
        dataset = Datasets.get_dataset(id)
        click.echo(dataset.get_dataset_info())
    else:
        dataset = Datasets.get_local_dataset(dataset_id)
        click.echo(dataset)
    
    
@click.command(name="columns")
@click.option('--id', required=True, help='Dataset ID')
def dataset_columns(id):
    click.secho("\n[+] Collecting columns from the dataset\n", fg='blue', bold=True)
    
    dataset = Datasets.get_dataset(id)
    click.echo(dataset.get_column_names())
    
    
@click.command(name="download")
@click.option('--id', required=True, help='Dataset ID')
@click.option('--path', required=True, help='Path where the downloaded dataset will be saved')
def dataset_download(id, path):
    click.secho("\n[+] Downloading dataset\n", fg='blue', bold=True)
    dataset = Datasets.get_dataset(id)
    dataset.download(path)


@click.command(name="add")
@click.option('--name', required=True, help='Path where the dataset to upload is located')
@click.option('--dir_path', required=True, help='Directory where the dataset to upload is located')
@click.option('--type', required=True, help='Dataset type. It should be hf, csv or json')
def dataset_add(name, dir_path, type):
    preferences = Preferences.load()

    type = type.strip()
    assert type in ["hf", "csv", "json"], "Dataset type should be hf, csv or json"
    dir_path = Path(dir_path)
    assert dir_path.is_dir(), "The path should be a directory"
    
    if preferences.current_mode == AppModes.CLOUD:
            dataset = Dataset(
                name=name,
                directory_path=dir_path,
                dataset_type=type
            )
            
            click.secho("\n[+] Uploading dataset...\n", fg='blue', bold=True)
            with Spinner():  
                dataset.upload()
            click.secho("\n[+] Dataset uploaded\n", fg='green', bold=True)
    else:
        dataset = LocalDataset(
            name=name,
            directory_path=dir_path,
            dataset_type=type
        )
        click.secho("\n[+] Uploading dataset...", fg='blue', bold=True)
        with Spinner(): 
            dataset.add()
        click.secho("[+] Dataset uploaded\n", fg='green', bold=True)


@click.command(name="remove")
@click.option('--id', help='ID of the dataset to be deleted')
def dataset_remove(id):
    preferences = Preferences.load()

    if preferences.current_mode == AppModes.LOCAL:
        dataset = Datasets.get_local_dataset(id)
        click.echo("Deleting the following dataset:")
        click.echo(id)

        click.confirm('Do you want to continue?', abort=True)

        Datasets.remove_local_dataset(id)
        click.echo("Deleted dataset")


datasets.add_command(ls_datasets)
datasets.add_command(dataset_inspect)
datasets.add_command(dataset_download)
datasets.add_command(dataset_add)
datasets.add_command(dataset_remove)
datasets.add_command(dataset_columns)