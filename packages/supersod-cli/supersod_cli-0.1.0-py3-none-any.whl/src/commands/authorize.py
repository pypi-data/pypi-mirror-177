import keyring
from click import secho, confirm

VALID_KEY_NAMES = ("ONFLEET_DEV", "AZURE_ADMIN", "GOOGLE_GEOCODING")


def auth(name: str, key: str, check: bool):
    if not any((name, check, key)):
        secho('No parameters supplied. See --help for usage.', err=True)
    if name not in VALID_KEY_NAMES:
        secho(f"WARNING: {name} is not a valid key name. Valid key names are: {VALID_KEY_NAMES}", bg='yellow')

    current_key = keyring.get_password('onfleet', name)

    if key and current_key:
        secho(f"Key {name} already set and will be overwritten", bold=True)
        if confirm("Continue?"):
            keyring.set_password('onfleet', name, key)
            return
    elif key:
        keyring.set_password('onfleet', name, key)
        secho(f'Key "{name}" set.')
    current_key = keyring.get_password('onfleet', name)

    if check and current_key:
        secho(f"{name}: {current_key}")
    elif check:
        secho(f"No Onfleet key found. Set with supersod auth <NAME> -k <API_KEY_HERE>")
