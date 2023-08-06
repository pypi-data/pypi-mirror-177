"""Console script for summed."""
import os
import sys

import click
from typing_extensions import Required

import summed


@click.group()
# @click.argument("action", default="info", type=click.Choice(ACTIONS))
# @click.option("-dc", "--db-connection", help="Azure CosmosDB Connection string")
# @click.option(
#    "-sc", "--storage-connection", help="Connection string for Azure storage."
# )
# @click.option("-c", "--config", help="The configuration ")
# @click.argument("output_file", type=click.File("w"), default="-", required=False)
# def main(action, space, file, config, output_file):
@click.option(
    "-dc",
    "--db-connection",
    help="SumMed db connection string (Azure Cosmos DB)",
    envvar="SUMMED_DB_CONNECTION",
)
@click.pass_context
def main(context, db_connection):
    """SumMed - empower patients and caregivers to better understand medical information."""
    click.echo(f"Using db connection string: {db_connection}")
    context.ensure_object(dict)
    context.obj["db_connection"] = db_connection

    return 0


@main.command()
def info():
    """Prints info about the SumMed package."""
    click.echo(f"SumMed - version {summed.__version__}")


@main.command()
@click.option("-s", "--space", help="The space to list the files", default="default")
def list_files(space):
    """Lists all file in a SumMed Space."""
    click.echo(f"Listing files in {space}")


@main.command()
@click.option("-s", "--space", help="The space to upload the file", default="default")
# @click.option(
#    "-f", "--from", "from_", help="URL or local filename to upload", required=True
# ) from_,
@click.argument("filename", required=False)
def upload(space, filename):
    """Uploads a file to a SumMed Space."""
    click.echo(f"{filename} => {space}/{filename}")


@main.command()
@click.option(
    "-s", "--space", help="The space to download the file from", default="default"
)
@click.argument("filename")
def download(filename, space):
    """Downloads a file from a SumMed Space."""
    click.echo(f"{filename} from {space}")


@main.command()
@click.option(
    "-s",
    "--space",
    help="The target space",
    show_default="users default space",
    default="default",
    required=True,
)
@click.argument("filename")
@click.confirmation_option(prompt="Are you sure you want to delete ?")
def delete(filename, space):
    """Deletes a file from a SumMed Space."""
    click.echo(f"Delete '{filename}' from space '{space}'")


if __name__ == "__main__":
    #
    # auto_envvar_prefix = "SUMMED"
    # => set cli options thrpugh environment variables.
    # e.g.: --space my_space --->
    default_map = {
        "list_files": {"space": "default1"},
        "upload": {"space": "default2"},
        "download": {"space": "default3"},
        "delete": {"space": "default4"},
    }
    sys.exit(
        main(auto_envvar_prefix="SUMMED", default_map=default_map)
    )  # pragma: no cover
