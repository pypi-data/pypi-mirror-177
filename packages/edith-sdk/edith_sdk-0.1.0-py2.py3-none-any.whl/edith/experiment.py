
class Experiment(object):

    def __init__(self, exp_obj) -> None:
        self.exp_obj = exp_obj
        self.exp_id = exp_obj['uri']['id']
        self.name = exp_obj['name']
        self.identifier = exp_obj['uri']['sdk_identifier']

    def __str__(self) -> str:
        return f"Experiment: {self.name} | Identifier:{self.identifier}"

if __name__ == '__main__':

    exp = {"uri": {"id": 7, "sdk_identifier": "ab3f6ebe-c858-45c4-84a1-a2a52c7c4db4", "url": "http://localhost:8080/api/experiments/7/"}, "name": "exp_temp1", "desc": "", "tech_stack": {}, "confluence_link": "", "jira_link": "", "story_points": 5, "identifier": "ab3f6ebe-c858-45c4-84a1-a2a52c7c4db4", "created_by": {"id": 1, "username": "admin", "url": "http://localhost:8080/api/users/1/"}, "created_on": "2022-09-15T09:39:09.911126Z", "project": {"id": 8, "name": "PA Classification", "url": "http://localhost:8080/api/projects/1/"}}
    exp = Experiment(exp_obj=exp)


