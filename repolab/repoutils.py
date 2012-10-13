from collections import deque

def walk_file_nodes(dirnode):
    """Generator for all files in a vcs DirNode."""

    stack = deque(dirnode.nodes)
    while stack:

        node = stack.pop()
        if node.is_dir():
            stack.extend(node.nodes)
        else:
            yield node

def dir_get_last_changeset(dirnode):
    """Return the last changeset of a directory."""

    get_date = lambda node: node.last_changeset.date
    latest_file = max(walk_file_nodes(dirnode), key=get_date)
    return latest_file.last_changeset
