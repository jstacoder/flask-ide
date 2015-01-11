def filter_templates(name):
    if not name.startswith('_'):
        if not len(name.split('/')) > 1:
            return True
    return False
  