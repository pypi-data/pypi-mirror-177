import os
import yaml
from rich import print

settings_file_location = os.path.expanduser('~/.ssh/pfm.settings.yaml')
settings = {
    'show_schema_link': 'false',
    'wait_after_start': 0.5,
    'wait_after_stop': 0.5,
    'table_border': 'false',
    'show_pid': 'false',
    'schemas': {}
}


def load_settings():
    global settings, settings_file_location

    if not os.path.isfile(settings_file_location):
        save_settings()

    with open(settings_file_location, "r") as stream:
        try:
            loaded_settings = yaml.load(stream, Loader=yaml.BaseLoader)
            settings.update(loaded_settings)

            if loaded_settings != settings:
                save_settings()
        except yaml.YAMLError as exc:
            print(exc)


def save_settings():
    global settings, settings_file_location

    print(f"[b]Updating configuration file on '{settings_file_location}'[/b]")

    with open(settings_file_location, "w") as stream:
        try:
            yaml.dump(settings, stream)
        except yaml.YAMLError as exc:
            print(exc)


def session_from_schema(schema_name, forward_definition):
    session_definition = {
        'schema': schema_name,
        'hostname': forward_definition.get('hostname'),
        'type': forward_definition.get('type', 'local'),
        'local_host': forward_definition.get('local_host', '127.0.0.1'),
        'local_port': str(forward_definition.get('local_port', '-')),
        'remote_host': forward_definition.get('remote_host', '127.0.0.1'),
        'remote_port': str(forward_definition.get('remote_port')),
        'alias': forward_definition.get('alias', '').upper(),
        'link': forward_definition.get('link')
    }

    name = forward_definition.get('name')
    if not name:
        name_string = 'pfm_session|{schema}|{hostname}|{remote_host}|{remote_port}|{local_host}|{local_port}|{type}'
        name = name_string.format(**session_definition)

    session_definition['name'] = name

    return session_definition


def get_schemas():
    global settings

    return settings.get('schemas', {})


def get_schema(schema_name):
    schemas = get_schemas()
    schema = schemas.get(schema_name)

    # inspect(schema)
    return schema


def save_forward(forward_definition):
    schemas = get_schemas()

    schema_name = forward_definition['schema']
    if schema_name not in schemas:
        schemas[schema_name] = []

    session_definition = {
        'hostname': forward_definition.get('hostname'),
        'type': forward_definition.get('type'),
        'local_host': forward_definition.get('local_host', '127.0.0.1'),
        'local_port': str(forward_definition.get('local_port', forward_definition.get('remote_port'))),
        'remote_host': forward_definition.get('remote_host', '127.0.0.1'),
        'remote_port': str(forward_definition.get('remote_port')),
    }

    if session_definition not in schemas[schema_name]:
        schemas[schema_name].append(session_definition)
        save_settings()
