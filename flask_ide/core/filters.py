from flask import Markup
import os
import os.path as op
from markdown_checklist.extension import ChecklistExtension
try:
    from markdown import markdown as md2
except ImportError:
    from markdown2 import markdown as md2
from jinja2.filters import do_filesizeformat    

# Jinja

def size(pth):
    if op.exists(pth):
        return do_filesizeformat(os.stat(pth).st_size)
    return False

def _sorted(value):
  return sorted(value)

def page(lst):
    return get_pages(lst)

def get_pages(lst,per_page=10):
    rtn = []
    new_lst = list(reversed(lst))
    page_total = len(lst) / per_page
    if len(lst) % per_page != 0:
        page_total += 1
    pages = [list() for x in range(page_total)]
    count = 0
    for new_page in pages:
        while count != per_page:
            if new_lst:
                count += 1
                new_page.append(new_lst.pop())
            else:
                break
        count = 0                    
    return pages

def date(value):
    """Formats datetime object to a yyyy-mm-dd string."""
    return value.strftime('%Y-%m-%d')


def date_pretty(value):
    """Formats datetime object to a Month dd, yyyy string."""
    return value.strftime('%B %d, %Y')


def datetime(value):
    """Formats datetime object to a mm-dd-yyyy hh:mm string."""
    return value.strftime('%m-%d-%Y %H:%M')


def pluralize(value, one='', many='s'):
    """Returns the plural suffix when needed."""
    return one if abs(value) == 1 else many


def month_name(value):
    """Return month name for a month number."""
    from calendar import month_name
    return month_name[value]


def markdown(value):
    """Convert plain text to HTML."""
    return Markup(md2(value, extensions=[ChecklistExtension()]))

def split(value,symbol=' '):
    return value.split(symbol)
