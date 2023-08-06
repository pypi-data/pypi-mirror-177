from yarl import URL

from ..base_functions.base_functions import log, logger
from ..base_functions.data_classes import DomainItem
from ..client.client import Session


class SaintCrawler:
    def __init__(self, *, include_id=False):
        self.include_id = include_id

    async def fetch(self, session: Session, url: URL):
        domain_obj = DomainItem(url.host, {})
        await log("Starting scrape of " + str(url))

        try:
            soup = await session.get_BS4(url)
            link = URL(soup.select_one('video[id=main-video] source').get('src'))
            await domain_obj.add_to_album("Saint Loose Files", link, url)

        except Exception as e:
            logger.debug("Error encountered while handling %s", str(url), exc_info=True)
            await log("Error scraping " + str(url))
            logger.debug(e)

        await log("Finished scrape of " + str(url))

        return domain_obj
