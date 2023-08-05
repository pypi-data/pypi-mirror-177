from typing import Dict, Optional, Tuple, List
from dotenv import dotenv_values
import json
import tarfile
import tempfile
FLAG_KERAS_IMPORTED = False
try:
    # conditional import keras depending on whether its installed in env
    from tensorflow import keras
    FLAG_KERAS_IMPORTED = True
except:
    try:
        import keras
        FLAG_KERAS_IMPORTED = True
    except:
        pass

if __package__:
    from .session import EdithSession
    from .exceptions import *
    from .experiment import Experiment
    from .device_utils import *
    from .trial import Trial
    from .utils import *
    from .artifact_utils import *
else:
    from session import EdithSession
    from exceptions import *
    from experiment import Experiment
    from device_utils import *
    from trial import Trial
    from utils import *
    from artifact_utils import *
import os
import warnings
import math
from tqdm import tqdm


class Edith(object):

    def __init__(self, **kwargs) -> None:
        # load variables such as
        self.config = {
            **dotenv_values(None),
            **os.environ,  # override loaded values with environment variables
        }
        verify_env_settings(self.config)
        self.verbose = kwargs.get('verbose', True)
        self.detect_host_details = kwargs.get('detect_host_details', True)
        self.detect_env_details = kwargs.get('detect_env_details', True)
        self.project_identifier = self.config['EDITH_PROJECT']
        self.session = EdithSession(base_url=self.config['EDITH_URL'], token=self.config['EDITH_TOKEN'], **kwargs)
        check_api_compatibility(self.session)
        self.project = assert_access_to_project(self.session, self.project_identifier, verbose=self.verbose)
        self.current_experiment = None
        self.current_trial = None

    def create_experiment(self, name: str, desc: Optional[str] = None, tech_stack: Optional[Dict[str, str]] = None,
                          story_points: Optional[int] = 5) -> Experiment:
        if self.current_trial is not None:
            # check status of current trial, if its not stopped or aborted, warn the user
            _ = self.current_trial.fetch_trial_status()
            if self.current_trial.is_active():
                raise Exception("Cannot switch experiment when an active trial is going on")
        name = validate_name(name, name_for='experiment')
        exp_obj = self.session.post(f"projects/{self.project['uri']['id']}/experiments/", data={
            "name": name,
            "desc": desc,
            "tech_stack": json.dumps(tech_stack),
            "story_points": story_points
        })
        self.current_experiment = Experiment(exp_obj=exp_obj)
        return self.current_experiment

    def get_experiment_by_id(self, id: str) -> Experiment:
        if not (id is not None and len(id) > 5):
            raise InvalidExperimentId()
        exp_obj = self.session.get("experiments/lookup", params={'identifier': id})
        self.current_experiment = Experiment(exp_obj=exp_obj)
        return self.current_experiment

    def get_experiment_by_name(self, name: str) -> Experiment:
        name = validate_name(name=name, name_for='experiment')
        exp_dict = self.session.get("experiments/lookup", params={'name': name})
        self.current_experiment = Experiment(exp_obj=exp_dict)
        return self.current_experiment

    def start_trial(self, name: str, tranche: Optional[str] = None, host_details: Optional[Dict[str, str]] = None,
                    env_details: Optional[Dict[str, str]] = None, git_commit_id: Optional[str] = None,
                    dvc_commit_id: Optional[str] = None, dataset_identifier: Optional[str] = None,
                    params: Optional[Dict[str, str]] = {}) -> Trial:
        if self.current_trial is not None:
            raise Exception("Cannot start a new trial without stopping existing trial")
        if self.current_experiment is None:
            raise ExperimentNotDefined()
        if host_details is None and self.detect_host_details:
            host_details = fetch_host_details()
        if env_details is None and self.detect_env_details:
            env_details = fetch_env_details()
        trial_body = {
            "name": name,
            "tranche": tranche,
            "host_details": json.dumps(host_details if host_details else {}),
            "env_details": json.dumps(env_details if env_details else {}),
            "params": params,
            "git_commit_id": git_commit_id,
            "dvc_commit_id": dvc_commit_id,
            "dataset_identifier": dataset_identifier
        }
        trial_dict = self.session.post(f"experiments/{self.current_experiment.exp_id}/trials/", data=trial_body)
        self.current_trial = Trial(trial_dict, session=self.session)
        _ = self.current_trial.fetch_trial_status()
        return self.current_trial

    def get_trial_by_name(self, name: str, experiment: Experiment) -> Trial:
        if self.current_trial is not None:
            _ = self.current_trial.fetch_trial_status()
            if self.current_trial.is_active():
                raise Exception("Cannot fetch a new trial without stopping existing trial")
        if self.current_experiment is None:
            raise ExperimentNotDefined()
        trial_dict = self.session.get(f"experiments/{experiment.exp_id}/trials/lookup", params={'name': name})
        self.current_trial = Trial(trial_dict, session=self.session)
        _ = self.current_trial.fetch_trial_status()
        return self.current_trial

    def assert_sync_feasibility(self):
        if self.current_experiment is None:
            raise ExperimentNotDefined()
        if self.current_trial is None:
            raise Exception("Cannot perform logging without starting a trial")
        if self.current_trial is not None and (not self.current_trial.is_active):
            raise Exception("Cannot log to a closed trial")

    def update_trial_status(self, status: str):
        assert status in Trial.STATUS_OPTIONS
        self.assert_sync_feasibility()
        if not self.current_trial.is_active and status in Trial.STATUS_OPTIONS_ACTIVE:
            raise Exception("Cannot open a closed trial")
        self.session.patch(f"trials/{self.current_trial.trial_id}/", data={
            'status': status
        })

    def end_trial(self, has_error: bool):
        self.update_trial_status(Trial.STATUS_CRASHED if has_error else Trial.STATUS_COMPLETED)
        _ = self.current_trial.fetch_trial_status()

    def log_params(self, params: Dict[str, object]):
        self.assert_sync_feasibility()
        assert params is not None
        if len(params) == 0:
            warnings.warn("You logging an empty param dictionary")
        self.session.patch(f"trials/{self.current_trial.trial_id}/", data={
            'params': json.dumps(params)
        })

    def log_metrics(self, metrics: Dict[str, object], step: int):
        self.assert_sync_feasibility()
        assert metrics is not None
        if len(metrics) == 0:
            warnings.warn("You logging an empty metrics dictionary")
        _ = self.session.post(f"trials/{self.current_trial.trial_id}/steps/", data={
            "step_num": step,
            "metrics": json.dumps(metrics)
        })

    def log_metrics_summary(self, metrics: Dict[str, object]):
        self.assert_sync_feasibility()
        assert metrics is not None
        if len(metrics) == 0:
            warnings.warn("You logging an empty metrics summary dictionary")
        self.session.patch(f"trials/{self.current_trial.trial_id}/", data={
            'metrics': json.dumps(metrics)
        })

    def save_artifact(self, filepath: str):
        self.assert_sync_feasibility()
        if not os.path.exists(filepath):
            raise Exception('artifact does not exist')
        if os.path.isdir(filepath):
            raise Exception('artifact cannot be a directory')
        _, file_extension = os.path.splitext(filepath)
        object_name = os.path.basename(filepath)
        n_bytes = os.path.getsize(filepath)
        file_size_mib = round(n_bytes / (1024 * 1024), 2)
        if file_size_mib > ARTIFACT_SIZE_LIMIT:
            raise Exception('artifact exceeds the allowed size limit')
        if file_extension not in ARTIFACT_MAP:
            raise Exception('This artifact type is not supported by Edith')
        artifact_type = ARTIFACT_MAP[file_extension]
        artifact_dict = {
            "n_files": 1,
            "size": n_bytes,
            "object_name": object_name,
            "artifact_type": artifact_type,
        }
        if file_size_mib < 10:
            response = self.session.post(f"trials/{self.current_trial.trial_id}/artifacts/", data=artifact_dict)
            upload_to_s3(filepath, object_name, response)
        else:
            multi_part_s3_upload(self.session, self.current_trial.trial_id, artifact_dict, filepath)

    # def get_presigned_url(self, filepath: str):
    #     _, file_extension = os.path.splitext(filepath)
    #     object_name = os.path.basename(filepath)
    #     n_bytes = os.path.getsize(filepath)
    #     file_size_mib = round(n_bytes / (1024 * 1024), 2)
    #     if file_size_mib > ARTIFACT_SIZE_LIMIT:
    #         raise Exception('artifact exceeds the allowed size limit')
    #     if file_extension not in ARTIFACT_MAP:
    #         raise Exception('This artifact type is not supported by Edith')
    #     artifact_type = ARTIFACT_MAP[file_extension]
    #     response = self.session.post(f"trials/{self.current_trial.trial_id}/artifacts/", data={
    #         "n_files": 1,
    #         "size": n_bytes,
    #         "object_name": object_name,
    #         "artifact_type": artifact_type,
    #     })
    #     return response

    def save_model(self, model_dir: str):
        self.assert_sync_feasibility()
        if not os.path.exists(model_dir):
            raise Exception('model directory does not exist')
        if not os.path.isdir(model_dir):
            raise Exception('`model_dir` needs to be a directory')
        object_name = 'Servable.tar.gz'
        # get number of files in the folder
        servable_files = os.listdir(model_dir)
        n_root_files = len(servable_files)
        if n_root_files == 0:
            raise Exception('`model_dir` directory cannot be empty')
        size_in_bytes, metadata = collect_directory_metadata(model_dir)
        print('model metadata:')
        print(json.dumps(metadata, indent=4))
        file_size_mib = round(size_in_bytes / (1024 * 1024), 2)
        artifact_dict = {
            "n_files": n_root_files,
            "size": size_in_bytes,
            "object_name": object_name,
            "artifact_type": ARTIFACT_TYPE_SERVABLE,
            "artifact_metadata": json.dumps(metadata)
        }
        # compress the folder into a temporary gzip2 file & then upload
        print('compressing directory content')
        temp_file = None
        try:
            temp_file = tempfile.NamedTemporaryFile(suffix='.tar.gz', delete=False)
            # print('temp path:', temp_file.name)
            with tarfile.open(fileobj=temp_file, mode="w:gz", ) as tar:
                for fname in os.listdir(model_dir):
                    tar.add(os.path.join(model_dir, fname), arcname=fname)
            temp_file.flush()
            temp_file.close()
            print('compression complete, uploading...')
            # upload the compressed file to s3
            gzip_size_mib = round(os.path.getsize(temp_file.name) / (1024 * 1024), 2)
            if file_size_mib < 10:
                response = self.session.post(f"trials/{self.current_trial.trial_id}/artifacts/", data=artifact_dict)
                upload_to_s3(temp_file.name, object_name, response)
            else:
                # streaming_upload_to_s3(temp_file.name, object_name, response)
                multi_part_s3_upload(self.session, self.current_trial.trial_id, artifact_dict, temp_file.name)
            print('upload complete')
        except Exception as e:
            raise e
        finally:
            if temp_file:
                try:
                    os.remove(temp_file.name)
                except:
                    pass

    def log_model_summary(self, model: object):
        if not FLAG_KERAS_IMPORTED:
            raise Exception('Could not find tensorflow/keras installation in given env')
        if model.__class__ not in [keras.models.Model, keras.models.Sequential]:
            raise Exception('This feature is only supported for tensorflow/keras models as of now')
        model_txt = ''

        def print_fn(line):
            nonlocal model_txt
            model_txt = model_txt + line + '\n'
        model.summary(print_fn=print_fn)
        temp_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False)
        temp_file.write(model_txt)
        temp_file.flush()
        temp_file.close()
        file_n_bytes = round(os.path.getsize(temp_file.name) / (1024 * 1024), 2)
        object_name = "model_summary.txt"
        response = self.session.post(f"trials/{self.current_trial.trial_id}/artifacts/", data={
            "n_files": 1,
            "size": file_n_bytes,
            "object_name": object_name,
            "artifact_type": ARTIFACT_TYPE_TEXT,
        })
        upload_to_s3(temp_file.name, object_name, response)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.current_trial is not None and self.current_trial.is_active:
            self.end_trial(has_error=type != None)


if __name__ == '__main__':

    client = Edith(debug=False)
    # exp = client.create_experiment(name='hello edith')
    # exp_id = "ab3f6ebe-c858-45c4-84a1-a2a52c7c4db4"
    # exp = client.get_experiment_by_id(exp_id)
    _ = client.get_experiment_by_name("I am batman")
    # client.start_trial(name='trail-3', tranche='optuna-1', host_details={'test':2})
    # trial_name = 'trial-2'
    # trial = client.resume_trial_by_name(trial_name)
    trial = client.start_trial(name='trial-1', tranche="optuna-study-3")
    print('id:', trial.trial_id)
    client.log_params({
        'learning_rate': 0.02,
        'batch_size': 15,
        'epochs': 8,
        'dropout_rate': 0.2,
        "model": "dnn",
        'is_prunned': None,
        "structure": {
            "layers": 7,
            "activation": "sigmoid"
        }
    })
    # for i in range(1, 15):
    #     client.log_metrics({
    #         'train': {
    #             # 'f1_score': round(1 / (10 - i), 2),
    #             'acc': round(1 / (20 - i), 2),
    #             'loss': round(1 / i, 2)
    #         },
    #         'val': {
    #             # 'f1_score': round(1 / (10 - i) - 0.1, 2),
    #             'acc': round(1 / (16 - i), 2) - 0.01,
    #             'loss': round((1 / i) + 0.1, 2)
    #         }
    #     }, step=i)
    # client.log_metrics_summary({
    #     'train': {
    #         # 'f1_score': 0.89,
    #         'loss': 0.01,
    #         'acc': 0.82
    #     },
    #     'val': {
    #         # 'f1_score': 0.87,
    #         'loss': 0.03,
    #         'acc': 0.81
    #     }
    # })
    # client.end_trial(has_error=False)
    for i in range(1, 15):
        client.log_metrics({
            'train': {
                # 'f1_score': round(1 / (10 - i), 2),
                'acc': round(1 / (25 - i), 2),
                'loss': round(1 / i, 2)
            },
            'val': {
                # 'f1_score': round(1 / (10 - i) - 0.1, 2),
                'acc': round(1 / (24 - i), 2) - 0.01,
                'loss': round((1 / i) + 0.1, 2)
            }
        }, step=i)
    client.end_trial(has_error=False)
    print('done')
