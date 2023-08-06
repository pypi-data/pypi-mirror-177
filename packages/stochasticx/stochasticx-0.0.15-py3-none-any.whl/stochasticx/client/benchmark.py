import json
import time
from pathlib import Path
import os
import click

from stochasticx.utils.docker import exists_container, start_container, stop_and_remove_container
from stochasticx.utils.preferences import Preferences, AppModes
from stochasticx.benchmark.local_benchmark import LocalBenchmark
from stochasticx.models.models import Models
from stochasticx.constants.docker_images import DockerImages, ContainerNames
from stochasticx.utils.auth_utils import AuthUtils
import sys

preferences = Preferences.load()


@click.group(name="benchmarking")
def benchmarking():
    try:
        AuthUtils.get_auth_headers()
    except:
        sys.exit()


@click.command(name="start")
@click.option('--job_name', required=True, help='Directory where the model to upload is located')
@click.option('--model_id', required=True, help='Id of registered model')
@click.option('--task_type', required=True, help='Task type. It should be sequence_classification, token_classification, question_answering, summarization,translation')
@click.option('--task_name', required=True, help='Name of task: onnx_benchmark, nvfuser_benchmark, tensorrt_benchmark')
@click.option('--params_file', required=True, help='File with params for benchmarking like input information and server config')
def benchmarking_start(job_name, model_id, task_type, task_name, params_file):
    if not exists_container(ContainerNames.BENCHMARK) and preferences.current_mode == AppModes.LOCAL:
        click.secho("\n[+] We are configuring the environment for model benchmarking. If it is the first time, it will take some minutes\n", fg='yellow', bold=True)

        start_container(
            docker_image=DockerImages.BENCHMARK,
            ports={
                "3000": "5001",
            },
            container_name=ContainerNames.BENCHMARK,
            detach=True,
            gpu=True,
            volumes=['stochasticx:/vol'],
            network_links={"x-local": "x-local"}
        )

        time.sleep(5)

        click.secho("[+] Environment already configured\n", fg='green', bold=True)

    model = Models.get_local_model(model_id)
    with open(params_file) as f:
        params = json.load(f)
    if preferences.current_mode == AppModes.LOCAL:
        benchmark = LocalBenchmark(
            job_name=job_name,
            task_name=task_name,
            model_type=model.model_type,
            model_path=model.directory_path,
            task_type=task_type,
            params=params
        )
        click.echo("Benchmarking model...")
        print(benchmark.benchmark().text)
        click.echo("Done")

        if exists_container(ContainerNames.BENCHMARK):
            click.secho(f"[+] Stopping and removing {ContainerNames.BENCHMARK}", fg="blue", bold=True)
            stop_and_remove_container(ContainerNames.BENCHMARK)
            click.secho("[+] Removed", fg="green", bold=True)


benchmarking.add_command(benchmarking_start)
