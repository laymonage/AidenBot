"""
File mirroring module.

(c) 2018 - laymonage
"""

import os
import tempfile
from urllib.parse import quote
from .dropson import dbx_dl, dbx_ul, to_json, get_json

STATIC_TMP_PATH = os.path.join(os.getcwd(), 'static', 'tmp')
MIRROR_SETTINGS_PATH = os.getenv('MIRROR_SETTINGS_PATH', None)
MIRROR_SETTINGS = get_json(dbx_dl(MIRROR_SETTINGS_PATH))


def mirror_toggle(set_id):
    """Toggle file mirroring on or off."""
    try:
        MIRROR_SETTINGS[set_id] = not MIRROR_SETTINGS[set_id]
    except KeyError:
        MIRROR_SETTINGS[set_id] = False
    dbx_ul(to_json(MIRROR_SETTINGS), MIRROR_SETTINGS_PATH, overwrite=True)
    return ("File mirroring has been turned {}."
            .format('on' if MIRROR_SETTINGS[set_id] else 'off'))


def mirror(message_content, file_name, host_url, set_id):
    """Write message_content into disk."""
    try:
        if not MIRROR_SETTINGS[set_id]:
            return ''
    except KeyError:
        MIRROR_SETTINGS[set_id] = True

    with tempfile.NamedTemporaryFile(dir=STATIC_TMP_PATH, prefix='file-',
                                     delete=False) as temp:
        for chunk in message_content.iter_content():
            temp.write(chunk)
        tempfile_path = temp.name

    dist_path = tempfile_path + '-' + file_name
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    host_url = host_url.replace('http://', 'https://')

    return host_url + quote((os.path.join('static', 'tmp', dist_name)))
