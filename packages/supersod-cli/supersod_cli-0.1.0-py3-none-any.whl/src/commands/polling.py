import requests
import keyring
from click import secho
from requests.exceptions import ReadTimeout


def poll(days: int):
    hk = keyring.get_password('onfleet', 'AZURE_ADMIN')
    if not hk:
        secho("Azure Onfleet API Key not set. Set using:", bg="yellow")
        secho("$\tsupersod auth AZURE_ADMIN -k <API_KEY_HERE>", bold=True)
        return -1

    url = f"https://onfleet.azurewebsites.net/api/createtestjobs?code={hk}&clientId=default"
    payload = {"days": days}
    try:
        resp = requests.post(url, json=payload, timeout=20)
    except ReadTimeout as e:
        secho(f"CRITICAL ERROR.  REQUEST TIMED OUT.\n{e}", err=True)
        return -1

    secho(f"SENT REQ FOR INTERVAL OF {days} DAYS. STATUS CODE:")
    color = 'green' if resp.status_code == 200 else 'red'
    secho(f"{resp.status_code} | {resp.text}", fg=color)
    secho("Check Azure Logs for detailed job creation info:")
    secho("https://portal.azure.com/#@supersod.com/resource/subscriptions/f8bcada7-e825-42de-90ec-20458c189d01/"
          "resourcegroups/SingleOpsOperations/providers/Microsoft.Web/sites/onfleet/logStream", fg="blue")
