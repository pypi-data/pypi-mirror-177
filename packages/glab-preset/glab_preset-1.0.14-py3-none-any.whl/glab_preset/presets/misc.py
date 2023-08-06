import gitlab

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
