import functools
import shutil
from pathlib import Path

from ..logger import logger
from ..models import Quality

TMP_DIR_PATH = Path("Facilito") / ".tmp"
TMP_DIR_PATH.mkdir(parents=True, exist_ok=True)


def ffmpeg_required(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        if not shutil.which("ffmpeg"):
            logger.error(
                "ffmpeg is not installed. Install it with: brew install ffmpeg"
            )
            return
        return await func(*args, **kwargs)

    return wrapper


@ffmpeg_required
async def download_video(
    url: str,
    path: Path,
    quality: Quality = Quality.MAX,
    **kwargs,
):
    """
    Download a video from a HLS m3u8 URL using ffmpeg with authenticated cookies.

    :param str url: URL of the m3u8 playlist.
    :param Path path: Path to save the video (.mp4).
    :param Quality quality: Kept for API compatibility (ffmpeg picks best available).
    :param list[dict] cookies: Playwright cookies for authentication (default: None).
    :param bool override: Override existing file if exists (default: False).
    :param int threads: Number of threads to use (default: 10).
    """
    import asyncio
    from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

    cookies: list[dict] = kwargs.get("cookies", None) or []
    override: bool = kwargs.get("override", False)
    threads: int = kwargs.get("threads", 10)

    path.parent.mkdir(parents=True, exist_ok=True)

    if not override and path.exists():
        logger.info(f"[{path.name}] already exists, skipping.")
        return

    # Build cookie header string from Playwright session cookies
    cookie_parts = [
        f"{c['name']}={c['value']}"
        for c in cookies
        if any(
            domain in c.get("domain", "")
            for domain in ["codigofacilito", "video-storage"]
        )
    ]
    cookie_str = "; ".join(cookie_parts)

    user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    # Build ffmpeg headers block (all in one -headers flag to avoid empty arg issues)
    headers = f"User-Agent: {user_agent}\r\n"
    headers += "Referer: https://codigofacilito.com/\r\n"
    headers += "Origin: https://codigofacilito.com\r\n"
    if cookie_str:
        headers += f"Cookie: {cookie_str}\r\n"

    command = [
        "ffmpeg",
        "-loglevel",
        "error",
        "-progress",
        "-",
        "-nostats",
        "-headers",
        headers,
        "-i",
        url,
        "-c",
        "copy",
        "-threads",
        str(threads),
        "-bsf:a",
        "aac_adtstoasc",
    ]

    if override:
        command += ["-y"]
    else:
        command += ["-n"]

    command.append(path.as_posix())

    # We will only use rich to show the progress.
    # The progress bar is completely transient, so once finished, it disappears.
    try:
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        with Progress(
            SpinnerColumn(),
            TextColumn(
                "[bold blue]Downloading[/bold blue] [green]{task.description}[/green]"
            ),
            TextColumn("• {task.fields[info]}"),
            TimeElapsedColumn(),
            transient=True,
        ) as progress:
            task_id = progress.add_task(path.name, info="Starting...", total=None)

            size_mb = 0.0
            time_str = "00:00:00"
            speed_str = "0.0x"
            bitrate_str = "0kbits/s"

            while True:
                line = await process.stdout.readline()
                if not line:
                    break

                line_str = line.decode("utf-8").strip()
                if line_str.startswith("out_time="):
                    time_piece = line_str.split("=")[1]
                    if time_piece != "N/A":
                        time_str = time_piece.split(".")[0]
                elif line_str.startswith("total_size="):
                    size_piece = line_str.split("=")[1]
                    if size_piece.isdigit():
                        size_mb = int(size_piece) / (1024 * 1024)
                elif line_str.startswith("speed="):
                    speed_piece = line_str.split("=")[1]
                    if speed_piece != "N/A":
                        speed_str = speed_piece.strip()
                elif line_str.startswith("bitrate="):
                    bitrate_piece = line_str.split("=")[1]
                    if bitrate_piece != "N/A":
                        bitrate_str = bitrate_piece.strip()

                progress.update(
                    task_id,
                    info=f"[cyan]Size: {size_mb:.1f} MB[/cyan] | [magenta]Rate: {bitrate_str}[/magenta] | [yellow]Video Time: {time_str}[/yellow] | [blue]Speed: {speed_str}[/blue]",
                )

        await process.wait()

        if process.returncode == 0:
            logger.info(f"[{path.name}] downloaded successfully ✓")
        else:
            stderr_output = await process.stderr.read()
            logger.error(
                f"Error downloading [{path.name}] (ffmpeg exit code {process.returncode})"
            )
            if stderr_output:
                logger.error(f"FFmpeg error: {stderr_output.decode('utf-8').strip()}")

    except Exception as e:
        logger.exception(f"Error downloading [{path.name}]: {e}")
