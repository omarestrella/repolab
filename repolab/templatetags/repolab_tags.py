from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

register = template.Library()

@register.filter
def cut_commit_msg(msg, max_length=50):
    """
    Takes a full commit message and returns the first `max_length` characters
    of the first line.
    """

    first_line_length = msg.find("\n")
    if first_line_length == -1:
        first_line_length = len(msg)

    if first_line_length > max_length:
        return msg[0: max_length] + "..."
    else:
        return msg[0: first_line_length]

@register.filter
def path_breadcrumbs(path, repo_slug):
    path = filter(lambda x: x, map(escape, path.split('/')))
    changeset = 'master'  #XXX
    ret = []

    # Repo name
    if path:
        url = reverse('repo_changeset_url', kwargs={
            'slug': repo_slug,
            'changeset': changeset,
        })
        ret.append('<a href="{0}">{1}</a>&nbsp;/&nbsp;'.format(url, repo_slug))
    else:
        ret.append('{0}&nbsp;/&nbsp;'.format(repo_slug))

    # Path to current node
    for i, directory in enumerate(path[0:-1]):
        if not directory: continue
        url = reverse('repo_path_url', kwargs={
            'slug': repo_slug,
            'changeset': changeset,
            'path': '/'.join(path[0:i+1]),
        })
        ret.append('<a href="{0}">{1}</a>&nbsp;/&nbsp;'.format(url, directory))

    # Current node
    if path:
        ret.append(path[-1])

    return mark_safe(''.join(ret))
