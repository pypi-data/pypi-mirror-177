from base_client import BaseClient


if __name__ == '__main__':

    client = BaseClient(debug=False)
    client.create_experiment(name="I am batman")
    client.create_experiment(name="experiment 123")