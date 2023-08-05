if __package__:
    from .base_client import BaseClient
    from .nlp_client import NLPClient
    from .artifact_store import ArtifactStore
else:
    from base_client import BaseClient
    from nlp_client import NLPClient
    from artifact_store import ArtifactStore


__version__ = "0.1.0"
__author__ = 'Niraj Kale'
__credits__ = 'SDK for Edith MLops platform'