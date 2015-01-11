from htmlbuilder import html


def add_column(**kwargs):
    if 'offset' in kwargs:
        offset = kwargs.pop('offset')
    else:
        offset = None
    if 'push' in kwargs:
        push = kwargs.pop('push')
    else:
        push = None
    if 'pull' in kwargs:
        pull = kwargs.pop('pull')
    else:
        pull = None

    cls_fmt = 'col-{size}-{num} '
    extra_fmt = 'col-{size}-{extra}-{num} '

    cls = ''
    for size,num in kwargs.items():
        cls += cls_fmt.format(size=size,num=num)
        for extra in filter(None,[offset,push,pull]
