from typing import Dict
if __package__:
    from .session import EdithSession
else:
    from session import EdithSession

class Trial(object):

    STATUS_OPEN = 'open'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_CRASHED = 'crashed'

    STATUS_OPTIONS = [STATUS_OPEN, STATUS_IN_PROGRESS, STATUS_COMPLETED, STATUS_CRASHED]
    STATUS_OPTIONS_ACTIVE = [STATUS_OPEN, STATUS_IN_PROGRESS]
    STATUS_OPTIONS_VALID = [STATUS_OPEN, STATUS_IN_PROGRESS, STATUS_COMPLETED]

    def __init__(self, trial_dict: Dict[str, object], session:EdithSession) -> None:
        self.trial_dict= trial_dict
        self.trial_id = trial_dict['uri']['id']
        self.session = session
        self.status = None
        self.name = trial_dict['name']
    
    def fetch_trial_status(self):
        trial_dict = self.session.get(f"trials/{self.trial_id}")
        self.status = trial_dict['status']
        return self.status

    @property
    def is_active(self):
        return self.status in self.STATUS_OPTIONS_ACTIVE

    def __str__(self) -> str:
        return f"Trial: {self.name} | status: {self.status}"

    

    
