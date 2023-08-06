import json
import os
import time
from pathlib import Path

import click
import requests
from retry import retry
from rich import print

from . import utils

IA_ACCESS_KEY = os.getenv("IA_ACCESS_KEY")
IA_SECRET_KEY = os.getenv("IA_SECRET_KEY")


@click.command()
@click.argument("handle")
@click.option("-o", "--output-dir", "output_dir", default="./")
def cli(handle: str, output_dir: str):
    """Archive a URL in the Wayback Machine."""
    # Pull the source’s metadata
    site = utils.get_site(handle)

    assert IA_ACCESS_KEY
    assert IA_SECRET_KEY

    # Ask for a capture
    print(f"🏛 Requesting a Wayback Machine capture of {site['url']}")
    capture_data = _post(site["url"])

    # If we've got a message, we need to just give up now. They're not going to do it.
    if "message" in capture_data:
        print(capture_data["message"])
    else:
        # Get the result of the request
        tries = 1
        while True:
            # Give it a second (as recommended by the archive.org admins)
            print("Waiting 6 seconds to request our job's status")
            time.sleep(6)

            # Check in our capture
            status_url = f"https://web.archive.org/save/status/{capture_data['job_id']}"
            status_data = _get(status_url)

            # If it's a success, we're done
            if status_data["status"] == "success":
                print("Success!")
                capture_data.update(status_data)
                break
            elif status_data["status"] == "pending":
                # If it's not done, up our counter and restart the loop
                print("The capture is still pending.")
                tries += 1
                # Unless we're over out limit, then we quit
                if tries >= 11:
                    print("10 tries have failed. We’re done here.")
                    break
            elif status_data["status"] == "error":
                # If there's an error, end it now
                print("There's an error. Time to call it quits.")
                capture_data.update(status_data)
                break

    # Set the output path
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Write it out
    slug = site["handle"].lower()
    with open(output_path / f"{slug}.wayback.json", "w") as fp:
        json.dump(capture_data, fp, indent=2)


@retry(tries=3, delay=5, backoff=2)
def _get(url: str):
    r = requests.get(url)
    assert r.ok
    j = r.json()
    return j


@retry(tries=3, delay=10, backoff=2)
def _post(url: str):
    r = requests.post(
        "https://web.archive.org/save",
        headers={
            "Authorization": f"LOW {IA_ACCESS_KEY}:{IA_SECRET_KEY}",
            "Accept": "application/json",
        },
        data={
            "url": url,
            "capture_screenshot": "1",
            "skip_first_archive": "1",
            "capture_all": "1",
        },
    )
    return r.json()


if __name__ == "__main__":
    cli()
