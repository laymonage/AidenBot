"""
Dropbox and JSON helper module.

(c) 2018 - laymonage
"""

import json
import os
import dropbox

# Dropbox access token obtained from dropbox.com/developers
DROPBOX_ACCESS_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN', None)
DBX_CLIENT = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)


def dbx_dl(file_path, metadata=False):
    """
    Return a binary object downloaded from Dropbox.

    file_path (str): path to the file to be downloaded
    metadata (bool): if True, return the metadata of the file instead
    """
    if not metadata:
        return DBX_CLIENT.files_download(file_path)[1].content
    return DBX_CLIENT.files_download(file_path)[0]


def dbx_ul(content, file_path, overwrite=False):
    """
    Upload a file to Dropbox.

    content (obj): a binary object to be uploaded
    file_path (str): file path in Dropbox
    overwrite (bool): overwrite mode
    """
    mode = (dropbox.files.WriteMode.overwrite
            if overwrite
            else dropbox.files.WriteMode.add)
    DBX_CLIENT.files_upload(content, file_path, mode)


def dbx_ls(folder_path, sort=False, reverse=False, noext=False):
    """
    Return a list of files in a given Dropbox folder.

    folder_path (str): a Dropbox folder to list the files from
    sort (bool): sort alphabetically
    reverse (bool): sort in descending order (if sort is True)
    noext (bool): if True, do not use file extension
    """
    if noext:
        result = [file.name[:file.name.rfind('.')] for file in
                  DBX_CLIENT.files_list_folder(folder_path).entries]
    else:
        result = [file.name for file in
                  DBX_CLIENT.files_list_folder(folder_path).entries]
    if sort:
        return sorted(result, reverse=reverse)
    return result


def dbx_tl(file_path):
    """Return a temporary link to a file hosted on Dropbox."""
    try:
        return DBX_CLIENT.files_get_temporary_link(file_path).link
    except dropbox.exceptions.ApiError:
        raise KeyError("Not found!")


def to_json(obj, indent=4, encoding='utf-8'):
    """
    Return an encoded JSON string converted from obj.

    obj (list or dict): object to be converted and encoded
    indent (int): indentation for the JSON output
    encoding (str): encoding to be used
    """
    return json.dumps(obj, indent=indent).encode(encoding)


def get_json(json_str, encoding='utf-8'):
    """
    Return a list or dictionary converted from an encoded json_str.

    json_str (str): JSON string to be decoded and converted
    encoding (str): encoding used by json_str
    """
    return json.loads(json_str.decode(encoding))
