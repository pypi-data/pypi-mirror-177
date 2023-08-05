import os
import requests
if __package__:
    from .session import EdithSession
    from .exceptions import *
    from .artifact_utils import *
else:
    from session import EdithSession
    from exceptions import *
    from artifact_utils import *
from typing import Dict
import tarfile
import math
from tqdm import tqdm

SUPPORTED_API_VERSION = 0.1


def verify_env_settings(config: Dict[str, object]):
    required_configs = ['EDITH_URL', 'EDITH_TOKEN', 'EDITH_PROJECT']
    for config_name in required_configs:
        if not(config_name in config and len(config[config_name].strip()) > 1):
            raise InvalidEnvironmentConfig(f"Invalid value for config: {config_name}")


def check_api_compatibility(session: EdithSession):
    api_info = session.get("version")
    if api_info['api_version'] != SUPPORTED_API_VERSION:
        raise EdithSDKCompatibilityError('This is SDK is not compatible with configure EDITH API')


def assert_access_to_project(session: EdithSession, project_identifier: str, verbose: bool):
    project = session.get("projects/lookup", params={'identifier': project_identifier})
    tenant = project['tenant']
    if verbose:
        print(f'Accessing Edith Project: {tenant["name"]}/{project["name"]}')
    return project


def validate_name(name: str, name_for: str):
    if not (name is not None and len(name) >= 3):
        raise InvalidResourceName(f"Invalid name given for {name_for}")
    return name.strip()


def collect_directory_metadata(dirpath, recursion_depth=10):
    if recursion_depth < 0:
        raise Exception('Servable file structure is too parse to be stored using Edith')
    metadata = {}
    size = 0.0
    for fname in os.listdir(dirpath):
        fullpath = os.path.join(dirpath, fname)
        _, file_extension = os.path.splitext(fullpath)
        if file_extension == '.exe':
            raise Exception('exe files cannot be part of your servable/artifacts')
        if os.path.isfile(fullpath):
            size += os.path.getsize(fullpath)
            metadata[fname] = int(size)
        else:
            subsir_size, subdir_metadata = collect_directory_metadata(fullpath, recursion_depth - 1)
            size += subsir_size
            metadata[fname] = subdir_metadata
    return size, metadata


def upload_to_s3(filepath, object_name, edith_response):
    with open(filepath, 'rb') as f:
        files = {'file': (object_name, f)}
        s3_response = requests.post(edith_response['presigned_url'], data=edith_response['upload_fields'], files=files)
    if s3_response.status_code != 204:
        raise Exception('Something went wrong while uploading the artifact')


def download_from_s3(filepath, url, chunk_size=32 * 1024):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)


def extract_servable_content(tar_path, dest_dir):
    with tarfile.open(tar_path, mode='r:gz') as f:
        f.extractall(dest_dir)


def multi_part_s3_upload(session, trial_id, artifact_dict, filepath):
    n_bytes = os.path.getsize(filepath)
    resp_artifact = session.post(f"trials/{trial_id}/artifacts/multipart_create/", data=artifact_dict)
    artifact_id = resp_artifact['uri']['id']
    task_id = resp_artifact['multipart_task_id']
    n_parts = math.ceil(n_bytes / ARTIFACT_MULTI_PART_CHUNK_SIZE)
    resp_urls = session.post(f"artifacts/{artifact_id}/presigned_collection/", data={
        "task_id": task_id,
        "start": 1,
        "end": n_parts
    })
    url_items = list(resp_urls['url_map'].items())
    parts = []
    with open(filepath, 'rb') as f:
        for i in tqdm(range(n_parts), desc='uploading'):
            buffer = f.read(ARTIFACT_MULTI_PART_CHUNK_SIZE)
            part_no, signed_url = url_items[i]
            res_part = requests.put(signed_url, data=buffer)
            assert res_part.status_code == 200
            parts.append({'ETag': res_part.headers['Etag'], 'PartNumber': int(part_no)})
    resp_multipart_complete = session.post(f"artifacts/{artifact_id}/complete_multipart/", json={
        "task_id": task_id,
        "parts": parts
    })
