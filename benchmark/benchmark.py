# Download the sample files ... one
# Auto commenting on PR thoughts

import argparse
import bz2
import datetime
from pathlib import Path
import csv
from io import StringIO
import sys

csv.field_size_limit(sys.maxsize)
from eyecite import get_citations


class Benchmark(object):
    """"""

    def __init__(self):
        """"""
        self.size = None
        self.root = Path(__file__).parent.absolute()
        self.dfa = None
        self.dfb = None
        self.file_append = None
        self.now = datetime.datetime.now()
        self.times = []
        self.totals = []
        self.list_of_ids = []
        self.opinions = []
        self.count = 0
        self.fields = []
        self.branch = None


    def fetch_citations(self, row):
        """"""
        row_id = row[0]
        row = dict(zip(self.fields, row))
        non_empty_rows = [row[field] for field in self.fields if type(row[field]) == str]
        if len(non_empty_rows) == 0:
            return None

        self.list_of_ids.append(row_id)
        found_cites = []
        for op in non_empty_rows:
            found_citations = get_citations(op)
            cites = [cite.token.data for cite in found_citations if cite.token]
            found_cites.extend(cites)
        self.opinions.append(found_cites)
        self.count += len(found_cites)
        self.totals.append(self.count)
        self.times.append((datetime.datetime.now() - self.now).total_seconds())


    def unzip(self):
        """"""
        zipfile = bz2.BZ2File(Path.joinpath(self.root, "..", "one-percent.csv.bz2"))
        byte_content = zipfile.read()
        content = byte_content.decode()
        file = StringIO(content)
        csv_data = csv.reader(file, delimiter=",")
        self.fields = next(csv_data)
        for row in csv_data:
            self.fetch_citations(row)
        columns = ["OpinionID", "Time", f"Total", "Opinions"]
        rows = zip(self.list_of_ids, self.times, self.totals, self.opinions)
        with open(f"../outputs/plotted-{self.branch}.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            for row in rows:
                writer.writerow(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A test program.')
    parser.add_argument('--main', action='store_true')
    parser.add_argument('--branch')
    args = parser.parse_args()

    benchmark = Benchmark()
    benchmark.branch = args.branch
    benchmark.unzip()

