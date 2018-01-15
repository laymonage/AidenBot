'''
Dropbox and JSON helper module
(c) 2018 - laymonage
'''

import json
import os
import requests
import dropbox

# Dropbox access token obtained from dropbox.com/developers
dropbox_access_token = os.getenv('DROPBOX_ACCESS_TOKEN', None)
dbx = dropbox.Dropbox(dropbox_access_token)


def dbx_dl(file_path, metadata=False):
    '''
    Return a binary object downloaded from Dropbox.
    file_path (str): path to the file to be downloaded
    metadata (bool): if True, return the metadata of the file instead
    '''
    if not metadata:
        return dbx.files_download(file_path)[1].content
    return dbx.files_download(file_path)[0]


def dbx_ul(content, file_path, overwrite=False):
    '''
    Upload a file to Dropbox.
    content (obj): a binary object to be uploaded
    file_path (str): file path in Dropbox
    overwrite (bool): overwrite mode
    '''
    mode = (dropbox.files.WriteMode.overwrite
            if overwrite
            else dropbox.files.WriteMode.add)
    dbx.files_upload(content, file_path, mode)


def dbx_ls(folder_path, sort=False, reverse=False, noext=False):
    '''
    Return a list of files in a given Dropbox folder.
    folder_path (str): a Dropbox folder to list the files from
    sort (bool): sort alphabetically
    reverse (bool): sort in descending order (if sort is True)
    noext (bool): if True, do not use file extension
    '''
    if noext:
        result = [file.name[:file.name.rfind('.')]
                  for file in dbx.files_list_folder(folder_path).entries]
    else:
        result = [file.name
                  for file in dbx.files_list_folder(folder_path).entries]
    if sort:
        return sorted(result, reverse=reverse)
    return result


def dbx_tl(file_path):
    '''
    Return a temporary link to a file hosted on Dropbox.
    '''
    headers = {
        'Authorization': 'Bearer {}'.format(dropbox_access_token),
        'Content-Type': 'application/json',
    }
    data = '"path": "{}"'.format(file_path)
    data = '{' + data + '}'
    data = data.encode('utf-8')
    url = 'https://api.dropboxapi.com/2/files/get_temporary_link'
    return requests.post(url, headers=headers, data=data).json()['link']


def toJSON(obj, indent=4, encoding='utf-8'):
    '''
    Return an encoded JSON string converted from obj.
    obj (list or dict): object to be converted and encoded
    indent (int): indentation for the JSON output
    encoding (str): encoding to be used
    '''
    return json.dumps(obj, indent=indent).encode(encoding)


def getJSON(JSON_str, encoding='utf-8'):
    '''
    Return a list or dictionary converted from an encoded JSON_str.
    JSON_str (str): JSON string to be decoded and converted
    encoding (str): encoding used by JSON_str
    '''
    return json.loads(JSON_str.decode(encoding))
