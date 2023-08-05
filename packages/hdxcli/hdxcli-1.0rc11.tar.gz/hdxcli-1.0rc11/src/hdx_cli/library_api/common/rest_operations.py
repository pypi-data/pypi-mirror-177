from typing import Dict, Any
from io import StringIO 
import json
import requests

from .exceptions import HdxCliException

Headers = Dict[str, str]

MAX_TIMEOUT=30

def create(url: str, *,
           headers: Headers,
           body: Dict[str, Any]):
    result = requests.post(url, json=body,
                           headers=headers,
                           timeout=MAX_TIMEOUT)
    if result.status_code not in (201, 200):
        raise HdxCliException(f'Error creating: {result.status_code} ' +
                              f'Message: {result.content}')

def create_file(url: str, *,
           headers: Headers, 
           file_stream,
           remote_filename):
    result = requests.post(url, files={'file': file_stream}, data={'name': remote_filename},
                            headers=headers,
                            timeout=MAX_TIMEOUT)
    if result.status_code not in (201, 200):
        raise HdxCliException(f'Error creating: {result.status_code} ' +
                              f'Message: {result.content}')

def update_with_patch(url, *,
           headers,
           body):
    result = requests.patch(url,
                          json=body,
                          headers=headers,
                          timeout=MAX_TIMEOUT)
    if result.status_code != 200:
        raise HdxCliException(f'Error updating: {result.status_code} ' +
                              f'Message: {result.content}')

def update_with_put(url, *,
           headers,
           body):
    result = requests.put(url,
                          json=body,
                          headers=headers,
                          timeout=MAX_TIMEOUT)
    if result.status_code != 200:
        raise HdxCliException(f'Error updating: {result.status_code} ' +
                              f'Message: {result.content}')


def list(url, *,
         headers):
    result = requests.get(url,
                          headers=headers,
                          timeout=MAX_TIMEOUT)
    if result.status_code != 200:
        raise HdxCliException(f'Error listing: {result.status_code} ' +
                              f'Message: {result.content}')
    return json.loads(result.content)


def options(url, *,
         headers):
    result = requests.options(url,
                          headers=headers,
                          timeout=MAX_TIMEOUT)
    if result.status_code != 200:
        raise HdxCliException(f'Error listing: {result.status_code} ' +
                              f'Message: {result.content}')
    return json.loads(result.content)


def delete(url, *,
           headers):
    result = requests.delete(url,
                          headers=headers,
                          timeout=MAX_TIMEOUT)
    if result.status_code != 204:
        raise HdxCliException(f'Error deleting: {result.status_code} ' +
                              f'Message: {result.content}')
    return json.loads('{}')
