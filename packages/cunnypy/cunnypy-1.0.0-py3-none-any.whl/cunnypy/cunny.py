import random
from typing import Dict, List, Optional

from .classes import CunnyPyError, Post, Site
from .utils import get_posts, resolve_site


async def search(
    site: str,
    credentials: Optional[Dict] = None,
    tags: Optional[List[str]] = None,
    limit: Optional[int] = 10,
    page: Optional[int] = 1,
    gatcha: Optional[bool] = False,
) -> Optional[List[Post]]:
    """Search the booru you have chosen

    :param site: The booru you wish to search
    :param credentials: Any api credentials for the booru
    :param tags: Any tags you are wanting to search with
    :param limit: Limit of posts to fetch
    :param page: Which page to fetch posts from
    :param gatcha: Weather to get a random post or not
    :return: List of CunnyPy Posts or just one Post
    """

    # Get site
    site: "Site" = await resolve_site(site) if not isinstance(site, Site) else site

    # Hard limit
    if limit >= 1000:
        raise CunnyPyError("Limit cannot exceed 1000")

    # Gatcha related params
    if gatcha and site.random:
        tags.append("order:random")

    # Format tags
    tags = [tag.strip().lower().replace(" ", "_") for tag in tags]

    # Setup httpx params
    params = {"tags": tags, "limit": limit, "pid": page}
    if credentials:
        params.update(credentials)

    # Fetch the posts
    posts = await get_posts(site, params)

    return [random.choice(posts)] if gatcha else posts
