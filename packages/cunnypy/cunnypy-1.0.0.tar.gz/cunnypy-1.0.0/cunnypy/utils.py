import json
from pathlib import Path
from typing import List, Optional

from aiofiles import open
from httpx import AsyncClient

from .classes import BooruNotFound, Post, Site


async def resolve_site(site: str) -> Optional[Site]:
    """Function to find a from sites.json from an aliases or site name

    :param site: Name of site or alias
    :return: Cunnypy Site Object
    """
    site = site.lower()
    async with open(f"{Path(__file__).parent}/sites.json", "r", encoding="utf-8") as f:
        raw = await f.read()
        sites = json.loads(raw)

        for domain, info in sites.items():
            if site == domain or site == info.get("domain") or site in info.get("aliases"):
                return Site(domain, info)
        raise BooruNotFound("That booru does not exist")


async def get_posts(site: Site, params: dict) -> Optional[List[Post]]:
    """Function to fetch posts from a given Site

    :param site: Cunnypy Site object
    :param params: params to use with the http request
    :return: List of posts
    """
    __http = AsyncClient(follow_redirects=True)

    async with __http as c:
        res = await c.get(site.search_url, params=params)
        res.raise_for_status()

        # Thanks e621
        if res.text == "":
            return []

        data = res.json()

        # Because sites like doing things different
        if site.domain == "e621.net":
            data = data["posts"]
        if site.domain == "gelbooru.com":
            data = data["post"]

        # No posts found
        if not data:
            return []

        posts = [Post(p, site) for p in data]
        return posts
