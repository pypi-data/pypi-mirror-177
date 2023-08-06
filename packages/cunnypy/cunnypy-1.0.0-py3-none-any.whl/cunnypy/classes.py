import reprlib
from datetime import datetime
from typing import List

from aiofiles import open
from httpx import AsyncClient


class CunnyPyError(BaseException):
    pass


class BooruNotFound(CunnyPyError):
    pass


class Site:
    """Class to represent one of the sites"""

    def __init__(self, domain: str, info: dict):
        self.domain: str = domain
        self.aliases: List[str] = info.get("aliases")
        self.nsfw: bool = info.get("nsfw")
        self.search_url: str = f"https://{self.domain}{info.get('api').get('search')}"
        self.post_view: str = f"https://{self.domain}{info.get('api').get('postView')}"
        self.post_comments_view: str = f"https://{self.domain}{info.get('api').get('postComments')}"
        self.random: bool = info.get("random")


class Post:
    """Class to represent a post from an image board"""

    def __init__(self, payload: dict, site: Site):
        # Cross compatability with older Booru API's
        payload = {k.strip("@"): v for k, v in payload.items()}

        self.id = payload.get("id", 0)
        self.creator_id = payload.get("creator_id", 0)
        self.created_at = payload.get("created_at")
        self.file_url = payload.get("file_url")
        self.filename = payload.get("image")
        self.source = payload.get("source") or None
        self.hash = payload.get("md5")
        self.height = payload.get("height")
        self.width = payload.get("width")
        self.rating = payload.get("rating")
        self.has_sample = payload.get("has_sample", "false")
        self.has_comments = payload.get("has_comments", "false")
        self.has_notes = payload.get("has_notes", "false")
        self.has_children = payload.get("has_children", "false")
        self.tags = payload.get("tags")
        self.change = datetime.fromtimestamp(int(payload.get("change", 0)))
        self.directory = payload.get("directory")
        self.status = payload.get("status")
        self.locked = payload.get("post_locked", 0)
        self.score = payload.get("score", 0)
        self.post_view = f"{site.domain}{site.post_view}{self.id}"
        self._payload = payload
        self._site = site

    async def download(self, location: str) -> None:
        """Allows you to download the image of the post to a specified location

        :param location: Location to download to
        """
        async with open(f"{location}/{self.filename}") as f:
            async with AsyncClient() as client:
                res = await client.get(self.file_url)
                await f.write(str(res.content))

    def __str__(self):
        return self.file_url

    def __int__(self):
        return self.id

    def __repr__(self):
        rep = reprlib.Repr()
        return f"<Post(id={self.id}, filename={rep.repr(self.filename)}, owner={rep.repr(self.creator_id)})>"
