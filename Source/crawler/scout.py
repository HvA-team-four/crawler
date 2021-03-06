import asyncio
from time import sleep

from utilities import tor
from utilities.models import *
from utilities.url_util import get_urls_from_content, format_url
import utilities.log as log


# Add found URLs to the database if they are not being blocked by the content-block feature.
@db_session
def save_url(url):
    blocked_urls = select(b.value for b in Block if b.type == "Url" and b.active)[:]

    if not any(x for x in blocked_urls if x in url):
        result = select(p for p in Url if p.url == url).count()
        if result == 0:
        	if ".onion" in url:
	            url_object = Url(
	                url=url,
	                date_added=datetime.now()
	            )
	        else:
	        	print("{} is blocked".format(url) )
    else:
        log.info("URL: {} is blocked".format(url))

    commit()


# Update the URL which was being scraped
@db_session
def update_url(url):
    """The update_url function sets the date of scraped urls to now."""
    url_db = select(u for u in Url if u.id == url.id).get()
    url_db.date_scanned = datetime.now()


@db_session
def get_urls_from_database():
    """The get_urls_from_database function fetches 8 urls from the database that need to be scraped by the scout.
     The urls which are set with a priority in the database will be retrieved first.
     """
    return select(u for u in Url if u.date_scanned is None).order_by(desc(Url.priority_scan))[:8]


def get_urls_from_results(urls, results):
    urls_in_results = []
    for index, url in enumerate(urls):
        if type(results[index]) is not bytes:
            continue

        urls_in_content = get_urls_from_content(results[index])
        for url_in_content in urls_in_content:
            urls_in_results.append(format_url(url.url, url_in_content))

    return urls_in_results



@db_session(optimistic=False)
async def main(loop):
    log.debug('scout has been started')
    while True:
        urls = get_urls_from_database()
        # update urls immediately to avoid different instances crawling the same urls
        for url in urls:
            update_url(url)

        if len(urls) == 0:
            print("No URLs to be crawled, waiting for 60 seconds.")
            log.info('No URLs to be crawled, waiting for 60 seconds.')
            sleep(60)
            commit()
            continue

        results = await tor.get_content_from_urls(loop, urls)
        urls_from_content = get_urls_from_results(urls, results)

        for u in urls_from_content:
            if u is not None:
                save_url(u)
        print('Found ', len(urls_from_content), ' urls')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
