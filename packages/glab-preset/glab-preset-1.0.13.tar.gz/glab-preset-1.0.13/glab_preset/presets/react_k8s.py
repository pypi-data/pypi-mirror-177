import jsw_nx as nx
import gitlab
import click

from .misc import create_or_update


@click.command()
@click.option('--project_id', prompt=True, required=True, type=int)
@click.option('--yarn_registry', prompt=True, default=nx.getenv('ALO7_YARN_REGISTRY'))
@click.option('--aliyun_ci_registry_image', prompt=True, default=nx.getenv('ALIYUN_CI_REGISTRY_IMAGE'))
@click.option('--acr_app_username', prompt=True, default=nx.getenv('ACR_APP_USERNAME'))
@click.option('--acr_app_password', prompt=True, default=nx.getenv('ACR_APP_PASSWORD'))
def react_k8s(**kwargs):
  gl = gitlab.Gitlab(url=nx.getenv('ALO7_GITLAB_URL'), private_token=nx.getenv('GITLAB_TOKEN'))
  prj = gl.projects.get(kwargs['project_id'])

  vars = [
    {'key': 'YARN_REGISTRY', 'value': kwargs['yarn_registry']},
    {'key': 'ALIYUN_CI_REGISTRY_IMAGE', 'value': kwargs['aliyun_ci_registry_image']},
    {'key': 'ACR_APP_USERNAME', 'value': kwargs['acr_app_username']},
    {'key': 'ACR_APP_PASSWORD', 'value': kwargs['acr_app_password']},
  ]

  for item in vars:
    create_or_update(prj, item)
