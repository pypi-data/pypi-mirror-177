def create_or_update(prj, item):
  item_var = prj.variables.get(item['key'])
  if item_var:
    item_var.value = item['value']
    item_var.save()
  else:
    prj.variables.create(item)
