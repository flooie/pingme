# Download the sample files ... one
# Auto commenting on PR thoughts

# Beep Boop
import argparse
import bz2
import datetime
import glob
import io
from pathlib import Path
import csv
from io import StringIO
import sys

csv.field_size_limit(sys.maxsize)

# from eyecite import get_citations
# import pandas as pd
# import matplotlib.pyplot as plt
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
        row_id = row[0]
        # print(row_id)
        row = dict(zip(self.fields, row))
        # print(row)
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
        zipfile = bz2.BZ2File(Path.joinpath(self.root, "one-percent.csv.bz2"))

        byte_content = zipfile.read()
        content = byte_content.decode()
        file = StringIO(content)
        csv_data = csv.reader(file, delimiter=",")
        self.fields = next(csv_data)
        for row in csv_data:
            self.fetch_citations(row)
        columns = ["OpinionID", "Time", f"Total", "Opinions"]
        rows = zip(self.list_of_ids, self.times, self.totals, self.opinions)
        with open(f"plotted-{self.branch}.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            for row in rows:
                writer.writerow(row)

        # dfx.to_csv(Path.joinpath(self.root, "..", f"plotted-{self.branch}.csv"), sep=",")


    def plot_charts(self):
        """"""
        # self.dfA = pd.read_csv(Path.joinpath(self.root, "", "plotted_A.csv"))
        #
        # csv_files = glob.glob(Path.joinpath(self.root, f"*.csv").as_posix())
        # # self.dfB = pd.read_csv(csv_files[0])
        # self.dfB = pd.read_csv(Path.joinpath(self.root, "", "plotted_B.csv"))


        # print(self.dfA.head())
        # self.dfB.rename(columns={'Total': 'TotalB'}, inplace=True)
        # print(self.dfB.head())
        #
        # df = pd.merge_asof(self.dfA, self.dfB, on='Time')
        # df.plot(x="Time", y=["Total", "TotalB"])
        # # plt.show()
        # plt.savefig('foo.png')


    def compare_dataframes(self):
        """"""
        # dfA = pd.read_csv(Path.joinpath(self.root, "other", "plotted_A.csv"))
        # dfB = pd.read_csv(Path.joinpath(self.root, "plotted_B.csv"))
        #
        # # dfB.columns = dfB.columns.str.replace('Total', 'TotalB')
        #
        # head_count = min([len(dfA), len(dfB)])
        #
        # dfA = dfA.head(head_count)
        # dfB = dfB.head(head_count)
        #
        # del dfA['Time']
        # del dfB['Time']
        # dfB.loc[0, 'Opinions'] = ['15 U.S.C. 2']
        # # del dfA['Total']
        # del dfB['Total']

        # print(dfA.compare(dfB))

    def generate_report(self):
        """"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A test program.')
    parser.add_argument('--main', action='store_true')
    parser.add_argument('--branch')
    args = parser.parse_args()

    benchmark = Benchmark()
    benchmark.branch = args.branch
    benchmark.unzip()
    print(benchmark.branch)

    # print(get_citations("2021COA112"))
    # print(get_citations("2021COA112M"))
    # print(get_citations("2021 COA 112"))


    # if not args.main:
    #
    #     benchmark.plot_charts()
    #     benchmark.compare_dataframes()
    #     benchmark.generate_report()

