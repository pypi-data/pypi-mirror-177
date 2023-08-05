import tempfile
from typing import Dict, Optional, Tuple, List
import json
import os
import numpy as np

if __package__:
    from .base_client import Edith
    from .artifact_utils import *
    from .utils import *
else:
    from base_client import Edith
    from artifact_utils import *
    from utils import *


class EdithForNLP(Edith):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def log_report(self, report: Dict, report_name: str, artifact_type: str):
        self.assert_sync_feasibility()
        temp_file = None
        try:
            temp_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.tar.gz', delete=False)
            temp_file.write(json.dumps(report, indent=4))
            temp_file.flush()
            temp_file.close()
            report_n_bytes = os.path.getsize(temp_file.name)
            response = self.session.post(f"trials/{self.current_trial.trial_id}/artifacts/", data={
                "n_files": 1,
                "size": report_n_bytes,
                "object_name": report_name,
                "artifact_type": artifact_type,
            })
            upload_to_s3(temp_file.name, report_name, response)
        except Exception as e:
            raise e
        finally:
            if temp_file:
                try:
                    os.remove(temp_file.name)
                except:
                    pass

    def log_classification_report(self, report_name: str, report_dict: Dict[str, Dict[str, float]]) -> None:
        headers = ['item', 'precision', 'recall', 'f1-score', 'support']
        items = []
        for key, entry in dict.items(report_dict):
            if entry.__class__ is dict:
                entry['item'] = key
                if set(headers) == set(dict.keys(entry)):
                    items.append(entry)
                else:
                    raise Exception('Inconsistent headers found in report')
        report = {
            'headers': headers,
            'items': items
        }
        self.log_report(report, report_name=report_name, artifact_type=ARTIFACT_TYPE_SKLEARN_CLF)

    def log_confusion_matrix(self, report_name: str, matrix: np.ndarray, labels: List[str]) -> None:
        n_labels = len(labels)
        if matrix.shape != (n_labels, n_labels):
            raise Exception('Invalid confusion matrix was provided for logging')
        headers = ['label']
        headers.extend(labels)
        items = []
        for label, report_i in zip(labels, matrix.tolist()):
            report_dict = dict(list(zip(labels, report_i)))
            report_dict['label'] = label
            items.append(report_dict)
        report_data = {
            'headers': headers,
            'items': items
        }
        self.log_report(report_data, report_name=report_name, artifact_type=ARTIFACT_TYPE_SKLEARN_SL_CONF_MAT)

    def log_multilabel_classification_report(self, report_name: str, matrix: np.ndarray, labels: List[str], report_suffix: str = '') -> None:
        n_labels = len(labels)
        if matrix.shape != (n_labels, 2, 2):
            raise Exception('Invalid confusion matrix was provided for logging')
        report_data = []
        for label, report_2d in zip(labels, matrix.tolist()):
            headers = ['label', label, 'others']
            items = [
                [label, *report_2d[0]],
                ['others', *report_2d[1]]
            ]
            report_data.append({
                'label': label,
                'report': {
                    'headers': headers,
                    'items': items
                }
            })
        self.log_report(report_data, report_name=report_name, artifact_type=ARTIFACT_TYPE_SKLEARN_ML_CONF_MAT)
