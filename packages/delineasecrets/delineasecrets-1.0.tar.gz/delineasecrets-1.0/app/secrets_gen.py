""" Secrets Interface """
import os
import time
import json
import base64

SECRET_PATH=os.environ.get('SECRET_PATH', '/var/secret')
SECRET_FILENAME=os.environ.get('SECRET_NAME', 'thy.json')
ENV = os.environ.get('ENV')

RETRY_ENABLED = True


def read_secrets_json(secret_path: str, secret_filename: str) -> dict:
    """ Read secrets from json. """
    global RETRY_ENABLED
    data = {}
    retries = 3
    status = 1
    while True:
        try:
            with open(f'{secret_path}/{secret_filename}', encoding='utf-8') as thy_json:
                data = json.load(thy_json)
                status = 0
        except FileNotFoundError:
            print(f'Secret json file not found in {secret_path}/{secret_filename}!')
            status = 1
        except Exception as error:
            print(f'Unknown error: {error}.')
            status = 1
        if RETRY_ENABLED and retries > 0 and status != 0:
            print('Waiting for json secrets!')
            time.sleep(3)
            retries -= 1
            continue
        if RETRY_ENABLED and status != 0:
            RETRY_ENABLED = False
            print('Too many read retries... Disabling retries!')
        break
    return data


def lookup_secret(secret_name: str, secrets: dict) -> tuple:
    """ Lookup secret. """
    secret_key = ''
    find = False
    need_decode = False
    keys = secrets.keys()
    for key in keys:
        if key.endswith(f'{ENV}_{secret_name}'.lower()):
            secret_key = key
            find = True
            break
        if key.endswith(f'{ENV}_{secret_name}_base64'.lower()):
            secret_key = key
            find = True
            need_decode = True
            break
    return find, secret_key, need_decode


def decode_b64_secret(value: str) -> str:
    """ Decode b64 secret. """
    decoded_value = value
    try:
        decoded_value = base64.b64decode(value).decode('utf-8')
    except Exception as error:
        print(f'Error decoding secret: {error}')
    return decoded_value


def normalize_secret_value(value: str, need_decode: bool) -> str:
    """ Normalize secret value. """
    normalized_value = value
    if isinstance(value, str):
        normalized_value = json.loads(value)
    normalized_value = normalized_value.get('value', '')
    if need_decode:
        normalized_value = decode_b64_secret(normalized_value)
    return normalized_value


def get_secret(secret_name: str, secret_path: str = SECRET_PATH, secret_filename: str = SECRET_FILENAME) -> str:
    """ Get secret. """
    secrets = read_secrets_json(secret_path, secret_filename)
    find, secret_key, need_decode = lookup_secret(secret_name, secrets)
    secret_value = ''
    if find:
        secret_value = normalize_secret_value(secrets.get(secret_key, {}), need_decode)
        print(f'Secret "{secret_name}" value from Vault')
    else:
        secret_value = os.environ.get(secret_name, '')
        print(f'Secret "{secret_name}" value from env')
    return secret_value