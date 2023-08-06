import subprocess
import typing
from pathlib import Path

import click
from retry import retry
from rich import print

from . import utils


@click.command()
@click.argument("handle")
@click.option("-o", "--output-dir", "output_dir", default="./")
@click.option(
    "--bundle",
    "is_bundle",
    is_flag=True,
    default=False,
    help="The provided handle is a bundle",
)
def cli(handle: str, output_dir: str, is_bundle: bool = False):
    """Save the accessiblity JSON of a single site."""
    if is_bundle:
        site_list = utils.get_sites_in_bundle(handle)
        for site in site_list:
            _get_accessibility(site, output_dir)
    else:
        # Get metadata
        site = utils.get_site(handle)

        # Do the thing
        _get_accessibility(site, output_dir)


@retry(tries=3, delay=5, backoff=2)
def _get_accessibility(data: dict, output_dir: str):
    print(f":newspaper: Fetching a11y tree from {data['url']}")

    # Set the output path
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Shoot the shot
    command_list: typing.List[typing.Any] = [
        "shot-scraper",
        "accessibility",
        data["url"],
        "-o",
        str(output_path / f"{data['handle'].lower()}.accessibility.json"),
        "--timeout",
        str(60 * 1000 * 3),
    ]
    javascript = utils.get_javascript(data["handle"])
    if javascript:
        command_list.extend(["--javascript", javascript])
    subprocess.run(command_list)


if __name__ == "__main__":
    cli()
