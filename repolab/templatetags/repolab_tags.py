from django import template

from vcs.utils import annotate

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
def render_file(file_):
    """
    Calls vcs util to output pygments highlighted file
    """

    return annotate.annotate_highlight(file_, order=('ls', 'code'))
