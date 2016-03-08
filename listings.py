from logger import Logger
from writer import RencenterFileWriter
from fetcher import RencenterFetcher


def main():
    logger = Logger()
    fetcher = RencenterFetcher()
    writer = RencenterFileWriter()

    listings = fetcher.fetch_all()
    logger.success("Finished fetching listings")
    writer.write("output.tsv", listings)

if __name__ == '__main__':
    main()
