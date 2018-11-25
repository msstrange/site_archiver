import requests as r
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
from time import sleep
from os import path, makedirs
from gooey import Gooey, GooeyParser
import argparse
from pathlib import Path

def SiteArchiver(site, domains_to_scrape, file_path, wait_time):

    file_path = str(Path(file_path))

    if wait_time < 20:
        wait_time = 20

    already_scraped = set()

    if not path.exists(file_path):
        makedirs(file_path)

    def filter(link):

        if link == None:
            return False

        if link == '/':
            return False

        if link.startswith('javascript'):
            return False

        if '#' in link:
            link = link.split('#', 1)[0]

        if not isinstance(link, str):
            return false

        if link.startswith('/'):
            link = site + link

        if any(link == page for page in already_scraped):
            return False

        return any(domain in link for domain in domains_to_scrape)

    def scrape(page):

        sleep(wait_time)

        # Deal with relative links
        if page.startswith('/'):
            page = site + page

        if '#' in page:
            page = page.split('#', 1)[0]

        already_scraped.add(page)

        page_text = r.get(page).text

        local_path = file_path + '//' + page.replace(':', '(c').replace('/', '(s)').replace('.', '(d)') + '.html'

        with open(local_path, 'w+', encoding="utf-8") as file:
            file.write(page_text)

        link_text = [link.get('href') for link in bs(page_text, 'html.parser').find_all('a')]

        [scrape(link) for link in link_text if filter(link)]

    scrape(site)

@Gooey(program_name='Site Archiver Tool')
def main():
    parser = GooeyParser(description='Saves a copy of root site and all sites in directory.')

    parser.add_argument(metavar='Site', dest='site', help = 'Url of the site to saved.', type=str)
    parser.add_argument(metavar='Domains to include', dest='domains', help='Comma seperated list of domains to be archived.')
    parser.add_argument(metavar='File Path', dest='file_path', help = 'Folder where site will be saved.', widget="DirChooser", type=str)

    parser.add_argument(
        metavar='Wait Time', dest='wait_time', help = 'Number of seconds to wait between page requests.',
        type=int, default=20
    )

    args = parser.parse_args()

    SiteArchiver(
        site=args.site, domains_to_scrape=args.domains, file_path=args.file_path,
        wait_time=args.wait_time
    )

if __name__ == '__main__':
    # main()
    SiteArchiver(
        "http://www.scp-wiki.net", "scp-wiki.net", file_path="D:\scp_archives",
        wait_time=60
    )