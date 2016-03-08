import urllib2
from itertools import chain
from logger import Logger
from parser import RencenterDirectoryParser


class RencenterFetcher(object):
    def __init__(self):
        self.logger = Logger()
        self.parser = RencenterDirectoryParser()

    def fetch_all(self):
        """Fetches all pages and returns RencenterListings"""
        self.logger.info("Fetching all pages from alumni.rencenter.org...")
        # code golf, i could not resist for this simple parser project
        return list(chain.from_iterable([
            self.fetch_one(index) for index in xrange(1, 55)
        ]))

    def fetch_one(self, index):
        """Fetches one page, index 1 to 54 (or more)"""
        self.logger.info("Fetching page %i from alumni.rencenter.org..." % index)
        f = urllib2.urlopen('http://alumni.rencenter.org/?p=%i' % index)
        html = f.read()
        f.close()
        return self.parser.parse(html)
