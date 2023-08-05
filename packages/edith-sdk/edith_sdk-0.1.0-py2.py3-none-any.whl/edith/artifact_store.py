from typing import Dict, Optional, Tuple, List
from dotenv import dotenv_values
import os
import tempfile
import warnings

if __package__:
    from .session import EdithSession
    from .exceptions import *
    from .experiment import Experiment
    from .utils import *
    from .artifact_utils import *
else:
    from session import EdithSession
    from exceptions import *
    from experiment import Experiment
    from utils import *
    from artifact_utils import *


class Artifact(object):

    def __init__(self, **kwargs) -> None:
        self.uri = kwargs.get('uri',None)
        if not self.uri:
            raise InvalidArtfactURI()
        self.identifier = self.uri['identifier']
        self.name = kwargs['object_name']
        self.n_files = kwargs['n_files']
        self.size_in_bytes = kwargs['size']
        self.is_edith_compatiable_servable = kwargs['flag_is_edith_compatible']
        self.artifact_metadata = kwargs['artifact_metadata']


class ArtifactStore(object):

    def __init__(self, **kwargs) -> None:
        # load variables such as
        self.config = {
            **dotenv_values(None),
            **os.environ,  # override loaded values with environment variables
        }
        verify_env_settings(self.config)
        self.verbose = kwargs.get('verbose', True)
        self.project_identifier = self.config['EDITH_PROJECT']
        self.session = EdithSession(base_url=self.config['EDITH_URL'], token=self.config['EDITH_TOKEN'], **kwargs)
        check_api_compatibility(self.session)
        self.project = assert_access_to_project(self.session, self.project_identifier, verbose= self.verbose)
    
    def fetch_artifact_details(self, identifier:str)-> Artifact:
        artifact_dict = self.session.get("artifacts/lookup", params={'identifier': identifier})
        return Artifact(**artifact_dict)

    def download_artifact(self, artifact: Artifact, download_dir:str):
        artifact_dict = self.session.get(f"artifacts/{artifact.uri['id']}/download")
        object_name = artifact_dict["object_name"]
        artifact_type = artifact_dict["artifact_type"]
        flag_extract = artifact_type == ARTIFACT_TYPE_SERVABLE
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        if flag_extract:
            temp_file = tempfile.NamedTemporaryFile(suffix='.tar.gz', delete=False)
            download_from_s3(temp_file.name, artifact_dict["presigned_download_url"])
            temp_file.flush()
            temp_file.close()
            extract_servable_content(temp_file.name, download_dir)
            try:
                os.remove(temp_file.name)
            except:
                warnings.warn('Unable to clear seravable cache')
        else:
            filepath = os.path.join(download_dir, object_name)
            if os.path.exists(filepath):
                raise Exception('Artifact with same name already exists in download_dir')
            download_from_s3(filepath, artifact_dict["presigned_download_url"])

    def fetch_report(self, artifact: Artifact):
        raise NotImplementedError()

    def fetch_dataframe(self, artifact: Artifact=None):
        raise NotImplementedError()


if __name__ == '__main__':

    import json
    identifier = 'd65e2a4e-1a1f-4b9a-b1e9-59623c29d483'

    store = ArtifactStore()
    artifact = store.fetch_artifact_details(identifier=identifier)
    a = store.download_artifact(artifact, download_dir=None)
    print(json.dumps(a, indent=4))

