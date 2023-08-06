import os
from contextlib import contextmanager


@contextmanager
def network_share_auth(share, username=None, password=None, drive_letter='Y', verbose=False):
    """Context manager that mounts the given share using the given
    username and password to the given drive letter when entering
    the context and unmounts it when exiting."""
    drive_letter = drive_letter.upper()
    cmd_parts = ["NET USE %s: %s" % (drive_letter, share)]
    if password:
        cmd_parts.append(password)
    if username:
        cmd_parts.append("/USER:%s" % username)
    os.system(" ".join(cmd_parts))
    try:
        yield
    finally:
        if verbose:
            os.system("NET USE %s: /DELETE" % drive_letter)
        else:
            os.system("NET USE %s: /DELETE > NUL" % drive_letter)
