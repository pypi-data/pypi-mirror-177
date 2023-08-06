from datetime import datetime, timedelta
import sys

from onfleet import Onfleet
import keyring
from click import secho, confirm


class OnfleetTasks:
    def __init__(self):
        onfleet_key = keyring.get_password('onfleet', "ONFLEET_DEV")
        if not onfleet_key:
            secho("Onfleet API Key not set. Set using:", bg="yellow")
            secho("$\tsupersod auth ONFLEET_DEV -k <API_KEY_HERE>", bold=True)
            sys.exit(-1)
        self.onfleet = Onfleet(api_key=onfleet_key)

    def get_tasks(self, days_from=1, days_to=30):
        # IF days_from > 3 it won't get new tasks ???????????
        if days_from > 3:
            secho("DAYS FROM > 3 ... CANT GET NEW JOBS", bg='yellow')
        days_f = datetime.now() - timedelta(days=days_from)
        days_t = datetime.now() + timedelta(days=days_to)

        df_timestamp = days_f.timestamp()*1000
        dt_timestamp = days_t.timestamp()*1000

        tasks = self.onfleet.tasks.get(queryParams={'from': df_timestamp, 'to': dt_timestamp})['tasks']
        return tasks

    def clear_tasks(self, days_from=1, days_to=30):
        tasks = self.get_tasks(days_from, days_to)
        secho(f'About to delete {len(tasks)} tasks.', bg='red')
        if confirm('Continue?'):
            for task in tasks:
                self.onfleet.tasks.deleteOne(task['id'])
                time_created = datetime.fromtimestamp(task["timeCreated"]/1000).strftime("%Y-%m-%d %H:%M:%S")
                secho(f'Deleted task {task["id"]} | {task["destination"]["address"]["city"]} @ {time_created}')


if __name__ == "__main__":
    oft = OnfleetTasks()
    ts = oft.get_tasks(days_from=2)
    for t in ts:
        print(ts)
