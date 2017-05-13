# -*- coding: utf-8 -*-

import abc

import selenium.common
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from . import interfaces


class DownloadFailed(Exception):
    pass


class HttpError(Exception):
    pass


class title_not_equal(object):

    def __init__(self, title):
        self.title = title

    def __call__(self, web_driver):
        return self.title != web_driver.title


class Base(interfaces.IDownloadStrategy):

    __metaclass__ = abc.ABCMeta

    def __init__(self, web_driver, page_timeout):

        """
        Parameters
        ----------
        web_driver : selenium.webdriver.Chrome
        page_timeout : float
            Number of seconds to wait for the page to finish rendering.
        """

        self._web_driver = web_driver
        self._page_timeout = page_timeout

    def download(self, url):
        self._web_driver.get(url=url)

        try:
            self._confirm_rendered_page(timeout=self._page_timeout)
        except selenium.common.exceptions.TimeoutException:
            if self._confirm_server_error(timeout=self._page_timeout):
                raise HttpError
            else:
                raise DownloadFailed

        download_id = self.do_download()
        return download_id

    def _confirm_rendered_page(self, timeout):
        wait = WebDriverWait(self._web_driver, timeout=timeout or 0)
        condition = title_not_equal('Showdown!')
        wait.until(condition)

    def _confirm_server_error(self, timeout):
        wait = WebDriverWait(self._web_driver, timeout=timeout or 0)
        css_selector = 'body > div.ps-overlay > div > form > p:first-child'
        locator = (By.CSS_SELECTOR, css_selector)
        text_ = 'disconnected'
        condition = expected_conditions.text_to_be_present_in_element(
            locator=locator,
            text_=text_)
        try:
            wait.until(condition)
        except selenium.common.exceptions.TimeoutException:
            encountered_server_error = False
        else:
            encountered_server_error = True
        return encountered_server_error

    @abc.abstractmethod
    def do_download(self):
        pass

    def dispose(self):
        self._web_driver.quit()

    def __repr__(self):
        repr_ = '{}(web_driver={}, page_timeout={})'
        return repr_.format(self.__class__.__name__,
                            self._web_driver,
                            self._page_timeout)
