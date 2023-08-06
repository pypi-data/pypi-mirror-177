"""pync csr rm command"""
import typing as t

import typer

from quara.creds.cli.utils import get_manager


def rm_cmd(
    root: t.Optional[str] = typer.Option(
        None, "--root", "-r", help="Nebula root directory", envvar="PYNC_NEBULA_ROOT"
    ),
    config: t.Optional[str] = typer.Option(
        None,
        "--config",
        "-c",
        help="pync configuration file",
        envvar="PYNC_NEBULA_CONFIG",
    ),
    authority: str = typer.Option(
        None, "--ca", help="Name of CA used to sign the certificate"
    ),
    name: t.Optional[str] = typer.Option(
        None,
        "--name",
        "-n",
        help="Certificate signing request name. Current username is used when not provided.",
    ),
) -> None:
    """Remove certificate signing request by name"""
    manager = get_manager(config, root)

    name = name or manager.default_user
    # Gather list of authorities used to issue certificates
    if authority is None:
        authorities = list(manager.authorities)
    else:
        authorities = [authority]
    for authority in authorities:
        manager.storage.delete_signing_request(authority=authority, name=name)

    raise typer.Exit(0)
