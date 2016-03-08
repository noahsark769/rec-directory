from logger import Logger
from bs4 import BeautifulSoup
from collections import namedtuple


RencenterListing = namedtuple("RencenterListing", ["name", "address", "phone", "email", "website"])


def clean(string):
    return string.replace("&nbsp;", "").strip()


class RencenterDirectoryParser(object):
    def __init__(self):
        self.logger = Logger()

    def parse(self, content):
        """Accepts html content and returns a list of RencenterListings"""
        soup = BeautifulSoup(content, "html.parser")
        listings = soup.find("div", attrs={"class": "sabai-directory-listings-with-map-listings"})
        return [
            self._parse_listing(listing)
            for listing in listings.find_all("div", attrs={"class": "sabai-entity-bundle-type-directory-listing"})
        ]

    def _parse_listing(self, listing):
        return RencenterListing(
            name=self._name_from_listing(listing),
            address=self._address_from_listing(listing),
            phone=self._phone_from_listing(listing),
            email=self._email_from_listing(listing),
            website=self._website_from_listing(listing)
        )

    def _text_from_child(self, content, classname, tagname="div"):
        result = content.find(tagname, attrs={"class": classname})
        if result:
            return clean(result.text)
        return None

    def _name_from_listing(self, listing):
        return self._text_from_child(listing, "sabai-directory-title")

    def _address_from_listing(self, listing):
        return self._text_from_child(listing, "sabai-directory-location")

    def _phone_from_listing(self, listing):
        tel = listing.find("div", attrs={"class": "sabai-directory-contact-tel"})
        if tel:
            return clean(tel.find("span", attrs={"class": "sabai-hidden-xs"}).text)
        return None

    def _email_from_listing(self, listing):
        return self._text_from_child(listing, "sabai-directory-contact-email")

    def _website_from_listing(self, listing):
        return self._text_from_child(listing, "sabai-directory-contact-website")

    def _warn_if_empty(self, string):
        if not string or len(string) == 0:
            self.logger.warn("Unexpected empty string encountered")
        return string
