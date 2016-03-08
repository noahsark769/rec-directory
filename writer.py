import csv
from logger import Logger


class RencenterFileWriter(object):
    def __init__(self):
        self.logger = Logger()

    def write(self, filename, listings):
        """Accepts a list of RencenterListings and writes them to a TSV file."""
        self.logger.info("Writing results to %s" % filename)
        try:
            with open(filename, "wb+") as f:
                writer = csv.writer(
                    f,
                    delimiter='\t',
                    quotechar='|',
                    quoting=csv.QUOTE_MINIMAL
                )
                writer.writerow(["Biz name", "Address", "Phone", "Email", "Website"])
                for listing in listings:
                    writer.writerow(listing)  # since it's a tuple we can write it directly :)
        except OSError as e:
            self.logger.fatal("Error writing csv: %s" % e)
            return
        self.logger.success("Successfully wrote file.")
