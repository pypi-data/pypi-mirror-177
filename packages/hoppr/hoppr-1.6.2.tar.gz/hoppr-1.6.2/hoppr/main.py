"""
Framework for manipulating bundles for airgapped transfers.
"""
import logging
import sys
from pathlib import Path
from platform import python_version
from typing import List, Optional

from typer import Argument, Option, Typer, echo

from hoppr import __version__
from hoppr.configs.credentials import Credentials
from hoppr.configs.manifest import Manifest
from hoppr.configs.transfer import Transfer
from hoppr.processor import HopprProcessor

VERBOSE_OPTION = Option(
    False,
    "-v",
    "--debug",
    "--verbose",
    help="Enable debug output",
)

app = Typer()


@app.callback()
def verbose(
    verbose_flag: Optional[bool] = VERBOSE_OPTION,
):  # pylint: disable=unused-argument
    """
    Define, validate, and transfer dependencies between environments.
    """
    return verbose_flag


@app.command()
def bundle(
    manifest_file: Path = Argument(
        "manifest.yml",
        help="Path to manifest file",
        expose_value=True,
    ),
    credentials_file: Path = Option(
        None,
        "-c",
        "--credentials",
        help="Specify credentials config for services",
        envvar="HOPPR_CREDS_CONFIG",
    ),
    transfer_file: Path = Option(
        "transfer.yml",
        "-t",
        "--transfer",
        help="Specify transfer config",
        envvar="HOPPR_TRANSFER_CONFIG",
    ),
    log_file: Path = Option(
        None,
        "-l",
        "--log",
        help="File to which log will be written",
        envvar="HOPPR_LOG_FILE",
    ),
    verbose_flag: Optional[bool] = VERBOSE_OPTION,
):
    """
    Run the stages specified in the transfer config
    file on the content specified in the manifest
    """

    metadata_files = [manifest_file, transfer_file]

    if credentials_file is not None:
        Credentials.load_file(credentials_file)
        metadata_files.append(credentials_file)

    manifest = Manifest.load_file(manifest_file)
    transfer = Transfer.load_file(transfer_file)
    log_level = logging.DEBUG if verbose_flag else logging.INFO

    processor = HopprProcessor(transfer, manifest, log_level)
    processor.metadata_files = metadata_files

    result = processor.run(log_file)

    if result.is_fail():
        sys.exit(1)


@app.command()
def version(
    verbose_flag: Optional[bool] = VERBOSE_OPTION,
):  # pylint: disable=unused-argument
    """
    Print version information for `hoppr`
    """
    echo(f"Hoppr Framework Version: {__version__}")
    echo(f"Python Version: {python_version()}")


@app.command()
def validate(
    input_files: List[Path],
    credentials_file: Path = Option(
        None,
        "-c",
        "--credentials",
        help="Specify credentials config for services",
        envvar="HOPPR_CREDS_CONFIG",
    ),
    transfer_file: Path = Option(
        "transfer.yml",
        "-t",
        "--transfer",
        help="Specify transfer config",
        envvar="HOPPR_TRANSFER_CONFIG",
    ),
    verbose_flag: Optional[bool] = VERBOSE_OPTION,  # pylint: disable=unused-argument
):
    """
    Validate multiple manifest files for schema errors.
    """

    cred_config = None
    transfer_config = None  # pylint: disable="unused-variable"
    manifests = []  # pylint: disable="unused-variable"

    if credentials_file is not None:
        cred_config = Credentials.load_file(credentials_file)
    if transfer_file is not None:
        transfer_config = Transfer.load_file(transfer_file)

    manifests = [Manifest.load_file(file, cred_config) for file in input_files]


if __name__ == "__main__":  # pragma: no cover
    app()
