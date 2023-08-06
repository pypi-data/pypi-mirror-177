import click
import requests
import sys
import numpy as np
from pathlib import Path
import uuid
from stochasticx.constants.urls import CloudRoutes, get_cloud_url

from stochasticx.utils.docker import (
    start_container, 
    stop_and_remove_container,
    get_logs_container
)

from stochasticx.datasets.datasets import Datasets
from stochasticx.stable_diffusion.download_models import download_model_from_s3
from stochasticx.utils.logging import configure_logger
from stochasticx.deployment.deployments import (
    StableDiffusionDeployments,
    StableDiffusionDeployment
)

from stochasticx.utils.preferences import AppModes, Preferences
from stochasticx.constants.docker_images import DockerImages, ContainerNames
from stochasticx.utils.auth_utils import AuthUtils

# from stochasticx.utils.gpu_utils import is_nvidia_gpu_available


@click.group(name="local")
def local():
    try:
        AuthUtils.get_auth_headers()
    except:
        sys.exit()

@click.command(name="init")
def init():    
    try:
        AuthUtils.get_auth_headers()
    except:
        sys.exit()
            
    click.secho("[+] Starting stochasticx in your local environment", fg="blue", bold=True)
    click.secho("[+] If it is the first time you deploy the model, it might take some minutes to deploy it", fg="blue", bold=True)
    start_container(
        docker_image=DockerImages.LOCAL,
        ports={ 
            "5432": "5432", 
            "3000": "3000"
        },
        container_name=ContainerNames.LOCAL,
        detach=True,
        gpu=False,
        volumes=['stochasticx:/vol']
    )

    try:
        click.echo("[+] Setting up preferences...")
        preferences = Preferences.load()
        preferences.current_mode = AppModes.LOCAL
        Preferences.save(preferences)
    except:
        stop()
    
    click.secho("[+] x-local server running in the port 3000", fg="green", bold=True)
    # click.echo("[+] Using GPU: {}".format(is_nvidia_gpu_available()))


@click.command(name="logs")
def logs():
    click.secho("[+] Logs", fg="blue", bold=True)
    logs = get_logs_container(ContainerNames.LOCAL)
    click.secho(logs, fg="white", bold=True)


@click.command(name="stop")
def stop():
    click.secho("[+] Stopping and removing x-local", fg="blue", bold=True)
    stop_and_remove_container(ContainerNames.LOCAL)
    click.secho("[+] Removed", fg="green", bold=True)

local.add_command(init)
local.add_command(logs)
local.add_command(stop)
