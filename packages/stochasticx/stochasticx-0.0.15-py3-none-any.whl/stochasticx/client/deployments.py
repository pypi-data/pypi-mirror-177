from pathlib import Path
import time
import click

from stochasticx.deployment.deployments import (
    Deployment,
    Deployments,
    Instances,
    SequenceClassificationInfTask,
    QuestionAnsweringInfTask,
    TranslationInfTask,
    SummarizationInfTask,
    TokenClassificationInfTask
)

from stochasticx.models.models import Models
from stochasticx.utils.parse_utils import print_table
from stochasticx.utils.preferences import Preferences, AppModes
from stochasticx.utils.docker import (
    start_container, 
    exists_running_container,
    stop_and_remove_container,
    get_logs_container,
    get_open_ports_container,
    exists_container
)
from stochasticx.utils.gpu_utils import is_nvidia_gpu_available
from stochasticx.deployment.deployments import (
    LocalDeploymentsClient,
    LocalSequenceClassificationDeployment,
    LocalQuestionAnsweringDeployment,
    LocalTokenClassificationDeployment,
    LocalTranslationDeployment,
    LocalSummarizationDeployment,
    LocalTextGenerationDeployment
)
from stochasticx.constants.docker_images import DockerImages, ContainerNames
from stochasticx.utils.auth_utils import AuthUtils
import sys


@click.group(name="deployments")
def deployments():
    try:
        AuthUtils.get_auth_headers()
    except:
        sys.exit()

    preferences = Preferences.load()

    if not exists_running_container(ContainerNames.INFERENCE) and preferences.current_mode == AppModes.LOCAL:
        click.secho("\n[+] We are configuring the environment for inference. If it is the first time, it will take some minutes\n", fg='yellow', bold=True)

        start_container(
            docker_image=DockerImages.INFERENCE,
            ports={
                "5000": "5051",
                "8000": "9000",
                "8001": "9001",
                "8002": "9002"
            },
            container_name=ContainerNames.INFERENCE,
            detach=True,
            gpu=is_nvidia_gpu_available(),
            network_links={"x-local": "x-local"},
            volumes_from=["x-local"]
        )

        time.sleep(10)

        click.secho("[+] Environment already configured\n", fg='green', bold=True)


@click.command(name="ls")
def ls_deployments():
    preferences = Preferences.load()

    click.secho("\n[+] Collecting all deployments\n", fg='blue', bold=True)
    if preferences.current_mode == AppModes.LOCAL:
        columns, values = LocalDeploymentsClient.get_deployments()
    else:
        columns, values = Deployments.get_deployments(fmt="table")
    print_table(columns, values)
        
        
@click.command(name="inspect")
@click.option('--id', required=True, help='Deployment ID')
def inspect_deployment(id):
    click.secho("\n[+] Collecting information from this deployment\n", fg='blue', bold=True)
    
    deployment = Deployments.get_deployment(id)
    click.echo(deployment)
    
    if deployment is not None:
        click.echo("Instance used: {}".format(deployment.get_instance()))
        click.echo("Deployed model: {}".format(deployment.get_optimized_model()))
        
        
@click.command(name="status")
@click.option('--id', required=True, help='Deployment ID')
def deployment_status(id):
    deployment = Deployments.get_deployment(id)
    click.echo(deployment.get_status())
    
    
@click.group(name="deploy")
def deploy():
    pass


@click.command(name="delete") 
@click.option('--model_name_or_id', required=True, help='Model ID')
@click.option('--model_type', required=False, default="hf", show_default=True, help='Model ID')
def delete_deployment(model_name_or_id, model_type):
    preferences = Preferences.load()

    click.secho("\n[+] Deleting deployment...", fg='blue', bold=True)

    if preferences.current_mode == AppModes.LOCAL:
        LocalDeploymentsClient.delete_deployment(
            model_type=model_type,
            model_name=model_name_or_id
        )
    else:
        click.secho("\n[+] Command not available for cloud...", fg='red', bold=True)

    click.secho("\n[+] Deleted", fg='green', bold=True)

@click.command(name="sequence_classification")
@click.option('--model_name_or_id', required=True, help='Model ID')
@click.option('--model_type', required=False, default="hf", show_default=True, help='Model ID')
@click.option('--instance_type', required=False, default=None, help='Instance type')
@click.option('--max_batch_size', required=False, default=8, show_default=True, help='Maximum batch size')
@click.option('--max_seq_length', required=False, default=128, show_default=True, help='Maximum source length')
def sequence_classification(
    model_name_or_id,
    model_type,
    instance_type,
    max_batch_size,
    max_seq_length
):
    preferences = Preferences.load()

    click.secho("\n[+] Starting deployment...", fg='blue', bold=True)

    if preferences.current_mode == AppModes.LOCAL:
        LocalSequenceClassificationDeployment(
            model_name=model_name_or_id,
            type=model_type,
            cuda=is_nvidia_gpu_available(),
            user_params={
                "max_batch_size": max_batch_size,
                "max_seq_length": max_seq_length
            }
        ).start_deployment()
    else:
        task_type = SequenceClassificationInfTask(
            max_batch_size=max_batch_size,
            max_seq_length=max_seq_length
        )
        
        model = Models.get_optimized_model(model_name_or_id)
        
        deployment = Deployment()
        deployment.start_inference(
            model=model,
            task_type=task_type,
            instance_type=instance_type
        )
    
    click.secho("[+] Model deployed\n", fg='green', bold=True)


@click.command(name="question_answering")
@click.option('--model_name_or_id', required=True, help='Model ID')
@click.option('--model_type', required=False, default="hf", show_default=True, help='Model ID')
@click.option('--instance_type', required=False, default=None, help='Instance type')
@click.option('--max_batch_size', default=8, show_default=True, help='Maximum batch size')
@click.option('--max_seq_length', default=128, show_default=True, help='Maximum sequence length')
def question_answering(
    model_name_or_id,
    model_type,
    instance_type,
    max_batch_size,
    max_seq_length
):
    preferences = Preferences.load()

    click.secho("\n[+] Starting deployment...", fg='blue', bold=True)

    if preferences.current_mode == AppModes.LOCAL:
        LocalQuestionAnsweringDeployment(
            model_name=model_name_or_id,
            type=model_type,
            cuda=is_nvidia_gpu_available(),
            user_params={
                "max_batch_size": max_batch_size,
                "max_seq_length": max_seq_length
            }
        ).start_deployment()
    else:
        task_type = QuestionAnsweringInfTask(
            max_batch_size=max_batch_size,
            max_seq_length=max_seq_length
        )
        
        model = Models.get_optimized_model(model_name_or_id)
        
        deployment = Deployment()
        deployment.start_inference(
            model=model,
            task_type=task_type,
            instance_type=instance_type
        )
    
    click.secho("[+] Model deployed\n", fg='green', bold=True)


@click.command(name="summarization")
@click.option('--model_name_or_id', required=True, help='Model ID')
@click.option('--model_type', required=False, default="hf", show_default=True, help='Model ID')
@click.option('--instance_type', required=False, default=None, help='Instance type')
@click.option('--max_batch_size', default=8, show_default=True, help='Maximum batch size')
@click.option('--max_source_length', default=128, show_default=True, help='Maximum source length')
@click.option('--source_prefix', default='', show_default=True, help='Source prefix')
@click.option('--lang', default='en', show_default=True, help='Language')
def summarization(
    model_name_or_id,
    model_type,
    instance_type,
    max_batch_size,
    max_source_length,
    source_prefix,
    lang
):
    preferences = Preferences.load()

    click.secho("\n[+] Starting deployment...", fg='blue', bold=True)

    if preferences.current_mode == AppModes.LOCAL:
        LocalSummarizationDeployment(
            model_name=model_name_or_id,
            type=model_type,
            cuda=is_nvidia_gpu_available(),
            user_params={
                "max_batch_size": max_batch_size,
                "max_source_length": max_source_length,
                "lang": lang,
                "source_prefix": source_prefix
            }
        ).start_deployment()
    else:
        task_type = SummarizationInfTask(
            max_batch_size=max_batch_size,
            max_source_length=max_source_length,
            source_prefix=source_prefix,
            lang=lang
        )
        
        model = Models.get_optimized_model(model_name_or_id)
        
        deployment = Deployment()
        deployment.start_inference(
            model=model,
            task_type=task_type,
            instance_type=instance_type
        )
    
    click.secho("[+] Model deployed\n", fg='green', bold=True)


@click.command(name="translation")
@click.option('--model_name_or_id', required=True, help='Model ID')
@click.option('--model_type', required=False, default="hf", show_default=True, help='Model ID')
@click.option('--instance_type', required=False, default=None, help='Instance type')
@click.option('--max_batch_size', default=8, show_default=True, help='Maximum batch size')
@click.option('--max_source_length', default=128, show_default=True, help='Maximum source length')
@click.option('--source_prefix', default='', show_default=True, help='Source prefix')
@click.option('--src_lang', default='en', show_default=True, help='Source language')
@click.option('--tgt_lang', default='de', show_default=True, help='Target language')
def translation(
    model_name_or_id,
    model_type,
    instance_type,
    max_batch_size,
    max_source_length,
    source_prefix,
    src_lang,
    tgt_lang
):
    preferences = Preferences.load()

    click.secho("\n[+] Starting deployment...", fg='blue', bold=True)

    if preferences.current_mode == AppModes.LOCAL:
        LocalTranslationDeployment(
            model_name=model_name_or_id,
            type=model_type,
            cuda=is_nvidia_gpu_available(),
            user_params={
                "max_batch_size": max_batch_size,
                "max_source_length": max_source_length,
                "src_lang": src_lang,
                "tgt_lang": tgt_lang,
                "source_prefix": source_prefix
            }
        ).start_deployment()
    else:
        task_type = TranslationInfTask(
            max_batch_size=max_batch_size,
            max_source_length=max_source_length,
            source_prefix=source_prefix,
            src_lang=src_lang,
            tgt_lang=tgt_lang
        )
        
        model = Models.get_optimized_model(model_name_or_id)
        
        deployment = Deployment()
        deployment.start_inference(
            model=model,
            task_type=task_type,
            instance_type=instance_type
        )
    
    click.secho("[+] Model deployed\n", fg='green', bold=True)


@click.command(name="token_classification")
@click.option('--model_name_or_id', required=True, help='Model ID')
@click.option('--model_type', required=False, default="hf", show_default=True, help='Model ID')
@click.option('--instance_type', required=False, default=None, help='Instance type')
@click.option('--max_batch_size', default=8, show_default=True, help='Maximum batch size')
@click.option('--max_seq_length', default=128, show_default=True, help='Maximum source length')
def token_classification(
    model_name_or_id,
    model_type,
    instance_type,
    max_batch_size,
    max_seq_length
):
    preferences = Preferences.load()

    click.secho("\n[+] Starting deployment...", fg='blue', bold=True)

    if preferences.current_mode == AppModes.LOCAL:
        LocalTokenClassificationDeployment(
            model_name=model_name_or_id,
            type=model_type,
            cuda=is_nvidia_gpu_available(),
            user_params={
                "max_batch_size": max_batch_size,
                "max_seq_length": max_seq_length
            }
        ).start_deployment()
    else: 
        task_type = TokenClassificationInfTask(
            max_batch_size=max_batch_size,
            max_seq_length=max_seq_length
        )
        
        model = Models.get_optimized_model(model_name_or_id)
        
        deployment = Deployment()
        deployment.start_inference(
            model=model,
            task_type=task_type,
            instance_type=instance_type
        )

    click.secho("[+] Model deployed\n", fg='green', bold=True)


        
@click.group(name="instances")
def instances():
    pass


@click.command(name="ls")
def ls_instances():
    click.secho("\n[+] Collecting all instances\n", fg='blue', bold=True)
    columns, values = Instances.get_instance_types(fmt="table")
    print_table(columns, values)

        
        
deploy.add_command(sequence_classification)
deploy.add_command(question_answering)
deploy.add_command(token_classification)
deploy.add_command(summarization)
deploy.add_command(translation)

deployments.add_command(ls_deployments)
deployments.add_command(inspect_deployment)
deployments.add_command(deployment_status)
deployments.add_command(deploy)
deployments.add_command(delete_deployment)

instances.add_command(ls_instances)