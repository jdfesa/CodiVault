import re

from playwright.async_api import BrowserContext

from ..constants import VIDEO_BASE_URL, VIDEO_M3U8_URL
from ..errors import VideoError
from ..models import Video
from ..utils import is_video


async def fetch_video(context: BrowserContext, url: str) -> Video:
    VIDEO_ID_SELECTOR = "input[name='video_id']"
    COURSE_ID_SELECTOR = "input[name='course_id']"
    M3U8_PATTERN = r"\/hls\/.*?\.m3u8"

    if not is_video(url):
        raise VideoError()

    try:
        page = await context.new_page()
        m3u8_url = None

        async def intercept_request(request):
            nonlocal m3u8_url
            if ".m3u8" in request.url and "playlist" in request.url:
                m3u8_url = request.url

        page.on("request", intercept_request)

        await page.goto(url)

        # Wait a bit for the player to initialize and request the stream
        try:
            # First wait for the video player container
            await page.wait_for_selector(".video-js, video", timeout=10000)
        except Exception:
            pass

        # Give it a few extra seconds to ensure the m3u8 request triggers
        await page.wait_for_timeout(3000)

        if m3u8_url:
            url = m3u8_url
        else:
            # Fallback to the old method if interception failed
            course_id = await page.locator(COURSE_ID_SELECTOR).first.get_attribute(
                "value"
            )
            video_id = await page.locator(VIDEO_ID_SELECTOR).first.get_attribute(
                "value"
            )

            if not video_id or not course_id:
                raise VideoError()

            url = VIDEO_M3U8_URL.format(course_id=course_id, video_id=video_id)

    except Exception:
        raise VideoError()

    finally:
        await page.close()

    return Video(url=url)
