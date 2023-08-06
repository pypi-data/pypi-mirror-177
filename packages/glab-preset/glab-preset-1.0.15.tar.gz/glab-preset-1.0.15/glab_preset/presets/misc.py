import re

import gitlab
import os

"""
This is a sample preset for creating or updating project variables.
注意：`prj.variables.get(var_name)` 这个 `api` 如果 `var_name` 不存在会直接报错
"""


def create_or_update(prj, item):
  var_name = item.get('key')
  try:
    item_var = prj.variables.get(var_name)
    item_var.value = item.get('value')
    item_var.save()
  except gitlab.exceptions.GitlabGetError:
    prj.variables.create(item)


def get_version_from_pyproject():
  pyproject_toml = open('./pyproject.toml', 'r')
  version_re = r'version = "(.*)"'
  matches = re.findall(version_re, pyproject_toml.read())
  if len(matches) > 0:
    return matches[0]
  else:
    return '0.0.0'
