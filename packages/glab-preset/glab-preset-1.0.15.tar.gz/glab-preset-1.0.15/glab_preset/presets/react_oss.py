import jsw_nx as nx
import gitlab
import click

from .misc import create_or_update


@click.command()
@click.option('--project_id', prompt=True, required=True, type=int)
@click.option('--yarn_registry', prompt=True, default=nx.getenv('ALO7_YARN_REGISTRY'))
@click.option('--alibabacloud_access_key_id', prompt=True, default=nx.getenv('ALIBABACLOUD_ACCESS_KEY_ID'))
@click.option('--alibabacloud_access_key_secret', prompt=True, default=nx.getenv('ALIBABACLOUD_ACCESS_KEY_SECRET'))
@click.option('--alibabacloud_region_id', prompt=True, default=nx.getenv('ALIBABACLOUD_REGION_ID'))
def react_oss(**kwargs):
  gl = gitlab.Gitlab(url=nx.getenv('ALO7_GITLAB_URL'), private_token=nx.getenv('GITLAB_TOKEN'))
  prj = gl.projects.get(kwargs['project_id'])

  access_key_id = kwargs['alibabacloud_access_key_id']
  access_key_secret = kwargs['alibabacloud_access_key_secret']
  region_id = kwargs['alibabacloud_region_id']

  vars = [
    {'key': 'YARN_REGISTRY', 'value': kwargs['yarn_registry']},
    {'key': 'ALIBABACLOUD_ACCESS_KEY_ID', 'value': access_key_id},
    {'key': 'ALIBABACLOUD_ACCESS_KEY_SECRET', 'value': access_key_secret},
    {'key': 'ALIBABACLOUD_REGION_ID', 'value': region_id},
  ]

  for item in vars:
    create_or_update(prj, item)
