if __package__:
    from .base_client import Edith
    from .nlp_client import EdithForNLP
    from .artifact_store import ArtifactStore
else:
    from base_client import Edith
    from nlp_client import EdithForNLP
    from artifact_store import ArtifactStore


__version__ = "0.1.1"
__author__ = 'Niraj Kale'
__credits__ = 'SDK for Edith MLops platform'