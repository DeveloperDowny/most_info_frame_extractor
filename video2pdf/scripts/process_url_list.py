import subprocess
import time
from typing import Annotated, List, Optional

import typer

from video2pdf.utils.helper import Helper

app = typer.Typer()


def main(urls: List[str]):
    for url in urls:
        try:
            subprocess.run([
                "python",
                "/home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/main.py",
                "--input=youtube",
                f"--url={url}",
                "--cleanup"
            ])
            time.sleep(10)
        except:
            print("Exception occurred for: ", url)


@app.command()
def run(
    url_list: Annotated[
        Optional[str],
        typer.Option(help="Comma-separated list of YouTube video URLs")
    ] = None,
    playlist_url: Annotated[
        Optional[str],
        typer.Option(help="YouTube playlist URL")
    ] = None
):
    urls = []

    if playlist_url:
        urls.extend(Helper.get_video_urls_from_playlist(playlist_url))

    if url_list:
        urls.extend([url.strip() for url in url_list.split(",") if url.strip()])
    main(urls)


if __name__ == "__main__":
    typer.run(run)
