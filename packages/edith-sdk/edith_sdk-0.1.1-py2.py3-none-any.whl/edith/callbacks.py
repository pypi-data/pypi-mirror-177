from typing import Dict, Optional, Tuple, List
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

if not FLAG_KERAS_IMPORTED:
    print('Edith keras callback in not available')

if __package__:
    from .base_client import Edith
    from .nlp_client import EdithForNLP
    from .artifact_utils import *
    from .utils import *
else:
    from base_client import Edith
    from nlp_client import EdithForNLP
    from artifact_utils import *
    from utils import *

if FLAG_KERAS_IMPORTED:

    class KerasCallback(keras.callbacks.Callback, Edith, EdithForNLP):

        def __init__(self, *args, **kwargs) -> None:
            # super().__init__(**kwargs) Issue: Keras callback does not support cooperative inheritance ;(
            # Need to use old style of python parent class init
            keras.callbacks.Callback.__init__(self)
            Edith.__init__(self, **kwargs)
            self.close_trial_on_end = kwargs.get('close_trial_on_end', False)

        def on_train_begin(self, logs=None):
            self.assert_sync_feasibility()

        def on_train_end(self, logs=None):
            if logs and len(logs) > 0:
                self.log_metrics_summary(logs)
            if self.close_trial_on_end:
                self.end_trial(has_error=False)

        def on_epoch_begin(self, epoch, logs=None):
            pass

        def on_epoch_end(self, epoch, logs=None):
            self.log_metrics(logs, step=epoch)

if __name__ == '__main__':

    cb = KerasCallback(debug=False)
