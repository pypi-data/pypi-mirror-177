"""admin commands for cmem command line interface."""
import sys

import click

import jwt

from cmem.cmemc.cli import completion
from cmem.cmemc.cli.context import ApplicationContext
from cmem.cmemc.cli.utils import struct_to_table
from cmem.cmempy.api import (
    get_access_token, get_token
)
from cmem.cmemc.cli.commands import CmemcCommand, CmemcGroup
from cmem.cmemc.cli.commands.metrics import metrics
from cmem.cmemc.cli.commands.store import store
from cmem.cmemc.cli.commands.workspace import workspace
from cmem.cmempy.health import get_complete_status_info


@click.command(cls=CmemcCommand, name="status")
@click.option(
    "--key", "key",
    autocompletion=completion.status_keys,
    help="Get only specific key(s) from the status / info output. There are "
         "two special keys available: 'all' will list all available keys in "
         "the table, 'overall.healthy' with result in  UP in case all "
         "health flags are UP as well (otherwise DOWN)."
)
@click.option(
    "--enforce-table",
    is_flag=True,
    help="A single value with --key will be returned as plain text instead "
         "of a table with one row and the header. This default behaviour "
         "allows for more easy integration with scripts. This flag enforces "
         "the use of tabular output, even for single row tables."
)
@click.option(
    "--raw",
    is_flag=True,
    help="Outputs combined raw JSON output of the health/info endpoints."
)
@click.pass_obj
def status_command(app: ApplicationContext, key, enforce_table, raw):
    """Output health and version information.

    This command outputs version and health information of the
    selected deployment. If the version information can not be retrieved,
    UNKNOWN shown.

    In addition to that, this command warns you if the
    target version of your cmemc client is newer than the version of your
    backend and if the ShapeCatalog has a different version then your
    DataPlatform component.

    To get status information of all configured
    deployments use this command in combination with parallel.

    Example: cmemc config list | parallel --ctag cmemc -c {} admin status
    """
    _ = get_complete_status_info()
    if "error" in _["di"]:
        app.echo_debug(_["di"]["error"])
    if "error" in _["dp"]:
        app.echo_debug(_["dp"]["error"])
    if "error" in _["dm"]:
        app.echo_debug(_["dm"]["error"])
    if raw:
        app.echo_info_json(_)
        return
    if key:
        table = [
            line for line
            in struct_to_table(_)
            if line[0].startswith(key) or key == "all"
        ]
        if len(table) == 1 and not enforce_table:
            app.echo_info(table[0][1])
            return
        if len(table) == 0:
            app.echo_error(f"No values for key(s) {key}.")
            sys.exit(1)
        app.echo_info_table(
            table,
            headers=["Key", "Value"],
            sort_column=0
        )
        return
    table = [
        ("DP", _["dp"]["version"], _["dp"]["healthy"]),
        ("DI", _["di"]["version"], _["di"]["healthy"]),
        ("DM", _["dm"]["version"], _["dm"]["healthy"]),
        ("SHAPES", _["shapes"]["version"], _["shapes"]["healthy"]),
        (_["store"]["type"], _["store"]["version"], _["store"]["healthy"])
    ]
    app.echo_info_table(
        table,
        headers=["Component", "Version", "Status"],
        sort_column=0
    )
    app.check_versions()
    if _["shapes"]["version"] not in (_["dp"]["version"], "UNKNOWN"):
        app.echo_warning(
            "Your ShapeCatalog version does not match your DataPlatform "
            "version. Please consider updating your bootstrap data."
        )


@click.command(cls=CmemcCommand, name="token")
@click.option(
    "--raw",
    is_flag=True,
    help="Outputs raw JSON. Note that this option will always try to fetch "
         "a new JSON token response. In case you are working with "
         "OAUTH_GRANT_TYPE=prefetched_token, this may lead to an error."
)
@click.option(
    "--decode",
    is_flag=True,
    help="Decode the access token and outputs the raw JSON. Note that the "
         "access token is only decoded and esp. not validated."
)
@click.pass_obj
def token_command(app, raw, decode):
    """Fetch and output an access token.

    This command can be used to check for correct authentication as well as
    to use the token with wget / curl or similar standard tools:

    Example: curl -H "Authorization: Bearer $(cmemc -c my admin token)"
    $(cmemc -c my config get DP_API_ENDPOINT)/api/custom/slug

    Please be aware that this command can reveal secrets, which you do not
    want to have in log files or on the screen.
    """
    # Note:
    # - get_access_token returns the token string which is maybe from conf
    # - get_token fetches a new token incl. envelope from keycloak

    if decode:
        token = get_access_token()
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        if raw:
            app.echo_info_json(decoded_token)
        else:
            table = struct_to_table(decoded_token)
            app.echo_info_table(
                table,
                headers=["Key", "Value"],
                sort_column=0
            )
    else:
        if raw:
            app.echo_info_json(get_token())
        else:
            token = get_access_token()
            app.echo_info(token)


@click.group(cls=CmemcGroup)
def admin():
    """Import bootstrap data, backup/restore workspace or get status.

    This command group consists of commands for setting up and
    configuring eccenca Corporate Memory.
    """


admin.add_command(status_command)
admin.add_command(token_command)
admin.add_command(metrics)
admin.add_command(workspace)
admin.add_command(store)
