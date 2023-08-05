import subprocess
from rich import inspect, print
from rich.table import Table
from . import tools
from .tools import settings
import time


def execute(command):
    # print(command)
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # inspect(result)
    # exit(1)
    if result.returncode != 0:
        print(f"Command [b]{command}[/] failed:\n {result.stderr}")
        exit(3)

    return result


def stop(session_definition):
    if is_active(session_definition):
        print("Stop {type} forward on [b]{hostname}[/b] {remote_host}:{remote_port}.".format(**session_definition))
        stop_commands = [
            'screen -ls',
            'grep "{name}"',
            'grep -i detached',
            'cut -d. -f1',
            'awk "{{print $1}}"',
            'xargs -I {{}} screen -XS "{{}}" quit'
        ]
        # stop_command = ' | '.join(stop_commands)
        # print(session_definition)
        stop_command = "tmux kill-session -t '{name}'".format(**session_definition)
        execute(stop_command)


def is_active(definition):
    sessions = get_active()

    # print(definition.get('name'))
    for session in sessions:
        shared_items = {k: session[k] for k in session if k in definition and session[k] == definition[k]}
        # print(len(shared_items))
        if len(shared_items) >= 7:
            # print(definition)
            # print(session)
            return True

    return False


def in_active_sessions(definition, active_sessions):
    for session in active_sessions:
        shared_items = {k: session[k] for k in session if k in definition and session[k] == definition[k]}
        # print(len(shared_items))
        if len(shared_items) >= 7:
            return True

    return False

def start(session_definition, reconnect: bool = False):
    if reconnect and is_active(session_definition):
        # print(f"[b]Stopping '{session_name}'[/b]")
        stop(session_definition)

    if not is_active(session_definition):
        print("Start {type} forward on [b]{hostname}[/b] {remote_host}:{remote_port}.".format(**session_definition))
        session_definition['shell_command'] = 'ping localhost'

        if session_definition.get('type') == 'remote':
            ssh = 'ssh -o ExitOnForwardFailure=yes -R {local_host}:{local_port}:{remote_host}:{remote_port} {hostname}'
        else:
            ssh = 'ssh -o ExitOnForwardFailure=yes -L {local_host}:{local_port}:{remote_host}:{remote_port} {hostname}'

        session_definition['ssh_command'] = ssh.format(**session_definition)

        # start_command = "screen -dmS '{name}' {ssh_command}  -- {shell_command}"
        start_command = "tmux new-session -d -s '{name}' '{ssh_command} -- {shell_command}'"
        # inspect(session_definition)
        result = execute(start_command.format(**session_definition))
        return result
    else:
        print("Ignoring {type} forward on [b]{hostname}[/b] {remote_host}:{remote_port}.".format(**session_definition))


def get_active():
    command = 'screen -ls | grep -i detached | cut -f2'
    command = "tmux ls | grep 'pfm_session' | cut -d ':' -f 1"
    result = execute(command)
    session_id_list = result.stdout.split("\n")

    sessions = []
    for session_id in session_id_list:
        if len(session_id) == 0:
            continue

        session_data = session_id.replace('_', '.').replace(':', '')
        # print(session_id)
        values = session_data.split('|')

        if len(values) == 8:
            filler, schema, hostname, remote_host, remote_port, local_host, local_port, forward_type = values

            session = {
                'schema': schema,
                'hostname': hostname,
                'type': forward_type,
                'remote_host': remote_host,
                'remote_port': remote_port,
                'local_host': local_host,
                'local_port': local_port,
                'name': session_id
            }

            # print(session)

            definition = get_session_definition(session)
            if definition:
                definition.update(session)
            else:
                definition = session

            sessions.append(definition)

    from operator import itemgetter
    sorted_sessions = sorted(sessions, key=itemgetter('schema'))

    return sorted_sessions


def filter_session(session, schema: str = None, host: str = None, port: str = None):
    if schema and schema not in session.get('schema'):
        return True
    if host and host not in session.get('hostname'):
        return True
    if port and port != session.get('local_port') and port != session.get('remote_port'):
        return True


def list_from_active(key, filter_string: str = ''):
    active_sessions = get_active()
    items = []
    for session in active_sessions:
        item = session.get(key)
        if filter_string not in item:
            continue
        if item not in items:
            items.append(item)

    return items


def prepare_table(show_alias: bool = False, show_link: bool = False, show_schema: bool = True, title: str = 'Schemas'):
    table = Table(show_edge=settings.get('table_border', 'false') == 'true')

    if show_schema:
        table.add_column("Schema", style="green", width=20)

    table.add_column("Hostname", justify="left", style="yellow", width=30)
    table.add_column("Type", justify="right", style="yellow", width=8)
    table.add_column("Local host", justify="right", style="white", width=15)
    table.add_column("Local port", justify="right", style="white", width=7)
    table.add_column("Remote host", justify="right", style="yellow", width=15)
    table.add_column("Remote port", justify="right", style="yellow", width=7)

    if show_alias:
        table.add_column("Alias", justify="right", style="cyan", width=10)

    if show_link:
        table.add_column("URL", style="cyan", width=60)

    return table


def show_active_sessions(schema: str = None, host: str = None, port: int = None):
    sessions = get_active()

    table = prepare_table(True, True)

    count = 0

    sorted_sessions = sorted(sessions, key=lambda d: d['schema'])

    for session in sorted_sessions:
        if filter_session(session, schema, host, port):
            continue
        count += 1

        last_row = False
        if count < len(sorted_sessions):
            if sorted_sessions[count]['schema'] != session['schema']:
                last_row = True

        row = [
            session.get('schema'),
            session.get('hostname'),
            session.get('type'),
            session.get('local_host'),
            session.get('local_port'),
            session.get('remote_host'),
            session.get('remote_port'),
            session.get('alias', '').upper(),
            session.get('link', '').format(**session),
        ]

        table.add_row(*row, end_section=last_row)

    if count > 0:
        print(table)
        if count == 1:
            message = f"[b]{count}[/b] active session.\n\n"
        else:
            message = f"[b]{count}[/b] active sessions.\n\n"
    else:
        message = f"Move along, nothing to see here."

    print(message)


def get_session_definition(session):
    schemas = tools.get_schemas()

    schema = schemas.get(session.get('schema'), [])
    for session_definition in schema:
        if session_definition.get('hostname') != session.get('hostname'):
            continue
        if session_definition.get('remote_port') != session.get('remote_port'):
            continue

        return session_definition

