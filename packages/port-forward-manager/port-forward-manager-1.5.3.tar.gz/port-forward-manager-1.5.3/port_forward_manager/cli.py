import pkg_resources
import random
import simplejson
from rich import print
import typer
import time

from .forward_sessions import prepare_table, show_active_sessions, in_active_sessions, get_active
from .cli_autocomplete import ac_schemas, ac_hosts
from .cli_autocomplete import sc_schemas, sc_hosts, ac_active_schemas, sc_active_remote_port, sc_active_hosts
from . import tools, forward_sessions


app = typer.Typer(no_args_is_help=True)
tools.load_settings()


@app.command()
def schemas(schema_filter: str = typer.Argument(None, autocompletion=ac_schemas),
            json: bool = typer.Option(False, '--json', '-j', help="Output JSON")):
    """
    List configured schemas
    """
    schema_list = list(tools.settings.get('schemas').keys())

    show_link = tools.settings.get('show_schema_link', 'false') == 'true'

    if not json:
        table = prepare_table(True, show_link, True)

    result_schemas = []
    result = {
        'schemas': result_schemas
    }

    active = get_active()

    for schema_name in schema_list:
        if schema_filter and schema_filter not in schema_name:
            continue

        schema = tools.get_schema(schema_name)
        count = 0
        for forward_definition in schema:
            count += 1
            session_definition = tools.session_from_schema(schema_name, forward_definition)
            del(session_definition['name'])

            if not json and not show_link:
                del (session_definition['link'])
            # del (session_definition['schema'])
            last_row = False
            if count == len(schema):
                last_row = True

            row = [
                session_definition.get('schema'),
                session_definition.get('hostname'),
                session_definition.get('type'),
                session_definition.get('local_host'),
                session_definition.get('local_port'),
                session_definition.get('remote_host'),
                session_definition.get('remote_port'),
                session_definition.get('alias')
            ]

            if json:
                session_definition['active'] = in_active_sessions(session_definition, active)
                link = session_definition.get('link')
                if link:
                    session_definition['link'] = link.format(**session_definition)
                result_schemas.append(session_definition),
            else:
                table.add_row(*row, end_section=last_row)
        # table.add_row(end_section=True)
    if not json:
        print(table)
    else:
        print(simplejson.dumps(result))


def generate_new_port(port_list):
    while True:
        port = str(random.randint(9100, 9500))
        if port not in port_list:
            port_list.append(port)
            return port


@app.command()
def start(schema_name: str = typer.Argument(..., autocompletion=ac_schemas),
          force: bool = typer.Option(None, help="Force sessions reconnection")):
    """
    Start a schema of forwarding sessions
    """
    schema = tools.get_schema(schema_name)
    active_ports = forward_sessions.list_from_active('local_port')
    if schema is None:
        print("[b]Schema '{0}' is unknown[/b]".format(schema_name))
        exit(-1)

    for forward_definition in schema:
        if 'local_port' not in forward_definition:
            new_port = generate_new_port(active_ports)
            forward_definition['local_port'] = new_port

        session_definition = tools.session_from_schema(schema_name, forward_definition)
        # print(session_definition)
        forward_sessions.start(session_definition, force)

    wait_time = float(tools.settings.get('wait_after_start', 0.5))
    time.sleep(wait_time)

    show_active_sessions()


@app.command()
def stop(schema: str = typer.Argument(None, autocompletion=ac_active_schemas),
         hostname: str = typer.Option(None, shell_complete=sc_active_hosts),
         port: str = typer.Option(None, shell_complete=sc_active_remote_port)):
    """
    Stop sessions from active schema, host or port
    """

    if not schema and not hostname and not port:
        print("[b]Pick a schema, host or host and port or --all[/b]")
        exit(-1)

    sessions = forward_sessions.get_active()
    for session in sessions:
        if forward_sessions.filter_session(session, schema, hostname, port):
            continue

        # print(session)
        session_definition = tools.session_from_schema(session['schema'], session)
        forward_sessions.stop(session_definition)

    wait_time = float(tools.settings.get('wait_after_stop', 0.5))
    time.sleep(wait_time)
    show_active_sessions()


@app.command()
def shutdown():
    """
    Stop all active sessions
    """

    sessions = forward_sessions.get_active()
    for session in sessions:
        session_definition = tools.session_from_schema(session['schema'], session)
        forward_sessions.stop(session_definition)

    show_active_sessions()


@app.command()
def forward(hostname: str = typer.Argument(..., autocompletion=ac_hosts),
            remote_port: int = typer.Argument(...),
            local_port: int = None,
            remote_host: str = '127.0.0.1',
            local_host: str = '127.0.0.1',
            remote: bool = False,
            schema: str = typer.Option('user-cli', shell_complete=ac_schemas), save: bool = False):
    """
    Start a forwarding session
    """

    if save and schema == 'user-cli':
        print("[b]To save, schema must be different from default 'user-cli'[/b]")
        exit(1)

    session_definition = {
        'hostname': hostname,
        'local_port': local_port or remote_port,
        'local_host': local_host,
        'remote_port': remote_port,
        'remote_host': remote_host,
        'type': 'remote' if remote else 'local'
    }

    forward_definition = tools.session_from_schema(schema, session_definition)
    forward_sessions.start(forward_definition)

    wait_time = float(tools.settings.get('wait_after_start', 0.5))
    time.sleep(wait_time)

    if save:
        tools.save_forward(forward_definition)

    show_active_sessions()


@app.command()
def status(schema: str = typer.Option(None, shell_complete=sc_schemas),
           host: str = typer.Option(None, shell_complete=sc_hosts),
           port: int = None,
           json: bool = typer.Option(False, '--json', '-j', help="Output JSON")):
    """
    Show active sessions
    """

    if json:
        sessions = forward_sessions.get_active()
        print(simplejson.dumps(sessions))
    else:
        show_active_sessions(schema, host, port)


@app.command()
def config():
    """
    Show active sessions
    """

    print(tools.settings)


@app.command()
def version():
    """
    Show active sessions
    """

    current_version = pkg_resources.get_distribution("port-forward-manager").version
    print(f"Port Forward Manager [bold white]v{current_version}[/]")


@app.command()
def state():
    result = forward_sessions.list_from_active('local_port')
    print(result)
def run():
    app()


if __name__ == "__main__":
    app()
