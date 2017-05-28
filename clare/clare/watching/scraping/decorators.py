# -*- coding: utf-8 -*-

from . import interfaces


class SerializedElements(interfaces.IDisposable, interfaces.IScraper):

    def __init__(self, scraper):

        """
        Parameters
        ----------
        scraper : clare.watching.scraping.scrapers.Base
        """

        self._scraper = scraper

    def scrape(self, url):
        elements = self._scraper.scrape(url=url)
        serialized_elements = [element.get_attribute('outerHTML')
                               for element
                               in elements]
        return serialized_elements

    def dispose(self):
        return self._scraper.dispose()

    def __repr__(self):
        repr_ = '{}(scraper={})'
        return repr_.format(self._scraper)