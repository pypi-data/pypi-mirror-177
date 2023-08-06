from pathlib import Path
import os
import click
import time

from stochasticx.utils.preferences import Preferences, AppModes
from stochasticx.conversion.local_conversion import LocalConversion
from stochasticx.models.models import Models
from stochasticx.utils.docker import (
    start_container,
    exists_container, stop_and_remove_container
)
from stochasticx.constants.docker_images import DockerImages, ContainerNames
from stochasticx.utils.auth_utils import AuthUtils
import sys

preferences = Preferences.load()

@click.group(name="conversion")
def conversion():
    try:
        AuthUtils.get_auth_headers()
    except:
        sys.exit()


@click.command(name="convert")
@click.option('--model_id', help='Directory where the model to upload is located')
@click.option('--convert_type', help='convert type. It should be onnx, tensorrt or onnx_int8')
@click.option('--model_type', help='Model type. It should be hf, pt or custom')
@click.option('--task_type', help='Task type. It should be sequence_classification, token_classification, question_answering, summarization,translation')
@click.option('--sequence_length', help='Sequence length should be specific for tensorrt conversion, not needed for onnx conversion')
@click.option('--max_batchsize', help='Maximum batch size should be specific for tensorrt conversion, not needed for onnx conversion')

def conversion_convert(model_id, convert_type, model_type, task_type, sequence_length, max_batchsize):
    if not exists_container(ContainerNames.CONVERSION) and preferences.current_mode == AppModes.LOCAL:
        click.secho("\n[+] We are configuring the environment for model conversion. If it is the first time, it will take some minutes\n", fg='yellow', bold=True)

        start_container(
            docker_image=DockerImages.CONVERSION,
            ports={ 
                "5000": "5000",
            },
            container_name=ContainerNames.CONVERSION,
            detach=True,
            gpu=True,
            volumes=['stochasticx:/vol']
        )

        time.sleep(5)

        click.secho("[+] Environment already configured\n", fg='green', bold=True)


    convert_type = convert_type.strip()
    assert convert_type in ["onnx", "tensorrt","onnx_int8"], "Conversion type should be onnx, tensorrt, onnx_int8"
    model = Models.get_local_model(model_id)
    model_path = Path(model.directory_path) #Path(path)
    if convert_type == "tensorrt" or convert_type == "onnx_int8":
        model_path = os.path.join(model_path,"model_onnx.onnx")
        #assert os.path.exists(model_path), "Can not find model_onnx.onnx in your provided directory"
    convert_params = {}
    if sequence_length is not None:
        convert_params["sequence_length"] = sequence_length
    if max_batchsize is not None:
        convert_params["max_batch_size"] = max_batchsize
    if preferences.current_mode == AppModes.LOCAL:
        
        model = LocalConversion(
            model_path=model_path,
            convert_type=convert_type,
            model_type=model_type,
            task_type=task_type,
            convert_params=convert_params
        )
        click.secho("\n[+] Converting model ...\n", fg='blue', bold=True)  
        model.convert()
        click.secho("\n[+] Model is converted\n", fg='green', bold=True)

        if exists_container(ContainerNames.CONVERSION):
            click.secho(f"[+] Stopping and removing {ContainerNames.CONVERSION}", fg="blue", bold=True)
            stop_and_remove_container(ContainerNames.CONVERSION)
            click.secho("[+] Removed", fg="green", bold=True)

conversion.add_command(conversion_convert)
