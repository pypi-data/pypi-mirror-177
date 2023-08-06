import csv
from datetime import datetime, timezone, timedelta
import sys

from onfleet import Onfleet
import requests
import keyring
from click import secho

stuart = [{
            "name": "Stuart Avera",
            "phone": "202-555-0127"
        }]


class Loader:
    def __init__(self):

        onfleet_key = keyring.get_password('onfleet', "ONFLEET_DEV")
        if not onfleet_key:
            secho("Onfleet API Key not set. Set using:", bg="yellow")
            secho("$\tsupersod auth ONFLEET_DEV -k <API_KEY_HERE>", bold=True)
            sys.exit(-1)

        self.google_key = keyring.get_password('onfleet', "GOOGLE_GEOCODING")
        if not self.google_key:
            secho("Google Geocoding API Key not set. Set using:", bg="yellow")
            secho("$\tsupersod auth GOOGLE_GEOCODING -k <API_KEY_HERE>", bold=True)
            sys.exit(-1)

        self.onfleet_api = Onfleet(api_key=onfleet_key)

    @staticmethod
    def get_delivery_window(_y: int, _m: int, _d: int, tz='est') -> tuple[float, float]:  # 4am and 9pm
        offset = 5
        if tz == 'cst':
            offset = 4
        _comp_after = datetime(_y, _m, _d, 4, tzinfo=timezone.utc) + timedelta(hours=offset)
        _comp_before = datetime(_y, _m, _d, 21, tzinfo=timezone.utc) + timedelta(hours=offset)
        return _comp_after.timestamp()*1000, _comp_before.timestamp()*1000

    def get_dest_from_coords(self, long: float, lat: float) -> dict:
        url = f"""https://maps.googleapis.com/maps/api/geocode/json?latlng=
                    {lat}, {long}&key={self.google_key}"""
        result = requests.get(url)
        print(result.json())
        return result.json()

    @staticmethod
    def make_task_payload(_city: str, _street_name: str, _street_num, _zipcode, _state: str,
                          _coords: list[float, float], recipients: list[dict], _complete_after,
                          _complete_before, _visit_id, _service_time, _quantity, _notes: str,
                          _color, _team: dict):
        task = {
            "destination": {
                "address": {
                    "city": _city,
                    "country": "United States",
                    "street": _street_name,
                    "number": str(_street_num),
                    "postalCode": str(_zipcode),
                    "state": _state
                },
                "location": _coords
            },
            "serviceTime": _service_time,
            "quantity": _quantity,
            "recipients": recipients,
            "appearance": {"triangleColor": _color},
            "completeAfter": _complete_after,
            "completeBefore": _complete_before,
            "notes": _notes,
            "container": _team
        }
        return task

    @staticmethod
    def make_task_payload_bm(_city: str, _coords: list[float, float], recipients: list[dict],
                             _complete_after, _complete_before, _visit_id, _service_time, _quantity, _notes: str,
                             _color, _team: dict):
        task = {
            "destination": {
                "address": {
                    "country": "United States",
                    "city": _city
                },
                "location": _coords  # long, lat
            },
            "serviceTime": _service_time,
            "quantity": _quantity,
            "recipients": recipients,
            "appearance": {"triangleColor": _color},
            "completeAfter": _complete_after,
            "completeBefore": _complete_before,
            "notes": _notes,
            "container": _team
        }
        return task

    def load_csv(self, filepath):
        with open(filepath, encoding='utf-8-sig') as f:
            task_reader = csv.DictReader(f)
            num_tasks = 0
            tasks_list = []
            for row in task_reader:
                # team container
                container = self.onfleet_api.containers.get(teams=row['teamassignment'])

                # time
                m, d, y = row['workstartdate'].split('/')
                comp_after, comp_before = self.get_delivery_window(int(y), int(m), int(d))

                # long / lat
                coordinates = [float(row['longitudecomplete']), float(row['latitudecomplete'])]

                # address
                addr = row['addresscomplete'].split()
                if not addr:
                    dest = self.get_dest_from_coords(*coordinates)
                    city = dest["results"][0]["address_components"][2]["long_name"]
                    task_payload = self. make_task_payload_bm(city, coordinates, stuart, comp_after, comp_before,
                                                              row['jobnumber'], row['servicetime'], row['capacity'],
                                                              row['taskdetails'], row['color'], container)
                else:
                    if addr[0].isdigit():
                        street_num = addr[0]
                        street_name = ' '.join(addr[1:])
                    else:
                        street_num = 1
                        street_name = row['addresscomplete']

                    # city
                    city = row['citycomplete']
                    if not city:
                        city = \
                            self. get_dest_from_coords(*coordinates)["results"][0]["address_components"][2]["long_name"]

                    # make payload
                    task_payload = self.make_task_payload(city, street_name, street_num, row['zipcomplete'],
                                                          row['statecomplete'], coordinates, stuart,
                                                          comp_after, comp_before, row['jobnumber'], row['servicetime'],
                                                          row['capacity'],  row['taskdetails'], row['color'], container)

                # make tasks
                # print(task_payload)
                tasks_list.append(task_payload)
                num_tasks += 1
        secho(f'Collected {num_tasks} tasks.', fg='green')
        return tasks_list, num_tasks

    def make_tasks(self, tasks: list):
        for task_payload in tasks:
            yield self.onfleet_api.tasks.create(body=task_payload)
        secho('Done.', fg='green')
