# Download the sample files ... one
# Auto commenting on PR thoughts

# Beep Boop

import bz2
import datetime
import io
from pathlib import Path

from eyecite import get_citations
import pandas as pd
import matplotlib.pyplot as plt


class Size:
    SMALL = 0
    LARGE = 1


class Benchmark(object):
    """"""

    def __init__(self):
        """"""
        self.size = None
        self.root = Path(__file__).parent.absolute()
        self.dfa = None
        self.dfb = None

    def unzip(self):
        """"""
        # if self.size:
        zipfile = bz2.BZ2File(Path.joinpath(self.root, "corpus", "one-percent.csv.bz2"))
        # else:
        #     zipfile = bz2.BZ2File(Path.joinpath(self.root, "corpus", "ten-percent.csv.bz2"))

        df = pd.read_csv(io.BytesIO(zipfile.read()))
        fields = list(df)[1:]

        # for part in ["A", "B"]:
        now = datetime.datetime.now()
        count = 0
        times = []
        totals = []
        opinion_ids = []
        opinions = []
        for row in df.iterrows():
            ops = [get_citations(row[1][x]) for x in fields if type(row[1][x]) == str]
            count += sum([len(x) for x in ops])
            opinion_ids.append(row[1][0])
            totals.append(count)
            opinions.append([" ".join(x[0].groups.values()) for x in ops if x])
            # print("\n\n")
            for op in ops:
                # print(len(op))
                if not len(op):
                    continue
                # print(op[0])
            times.append((datetime.datetime.now() - now).total_seconds())
            if (datetime.datetime.now() - now).total_seconds() > 10:
                break

        columns = ["OpinionID", "Time", f"Total", "Opinions"]
        dfx = pd.DataFrame(list(zip(opinion_ids, times, totals, opinions)), columns=columns)
        dfx.to_csv(Path.joinpath(self.root, "corpus", f"plotted.csv"), sep=",")

        return True

    def one_percent_sample(self):
        """"""
        self.size = Size.SMALL
        print(Path.joinpath(self.root, "corpus", "plotted.csv"))
        sample = self.unzip()

    def plot_charts(self):
        """"""
        self.dfA = pd.read_csv(Path.joinpath(self.root, "corpus", "plotted.csv"))
        # self.dfB = pd.read_csv(Path.joinpath(self.root, "corpus", "plottedB.csv"))

        # df = pd.merge_asof(self.dfA, self.dfB, on='Time')
        # df.plot(x="Time", y=["TotalA", "TotalB"])
        # plt.show()

    def compare_dataframes(self):
        """"""
        dfA = pd.read_csv(Path.joinpath(self.root, "corpus", "plotted.csv"))
        # dfB = pd.read_csv(Path.joinpath(self.root, "corpus", "plottedB.csv"))

        # head_count = min([len(dfA), len(dfB)])

        # dfA = dfA.head(head_count)
        # dfB = dfB.head(head_count)

        # del dfA['Time']
        # del dfB['Time']
        # del dfA['Total']
        # del dfB['TotalB']

        # print(dfA.compare(dfB))


if __name__ == "__main__":
    print("STARTING UP ---- new branch")
    Benchmark().one_percent_sample()

    # Benchmark().plot_charts()
    # Benchmark().compare_dataframes()
    print("SHUTTING DOWN ---- new branch")
