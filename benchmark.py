# Download the sample files ... one
# Auto commenting on PR thoughts

# Beep Boop

import bz2
import datetime
import glob
import io
import os
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
        self.file_append = None

    def unzip(self):
        """"""
        zipfile = bz2.BZ2File(Path.joinpath(self.root, "corpus", "one-percent.csv.bz2"))

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
        # import os
        # import glob

        # print("\n\n\n")
        # print(glob.glob("/home/runner/work/pingme/pingme/corpus/*"))
        # print("\n\n\n")

        # if os.path.exists("/home/runner/work/pingme/pingme/corpus/plotted_{}.csv"):
        #     # print("The file exists ... dont overwrite it.")
        dfx.to_csv(Path.joinpath(self.root, "corpus", f"plotted_A.csv"), sep=",")

        # else:
        #     # print("The file  A exists  B")
        #     dfx.to_csv(Path.joinpath(self.root, "corpus", f"plotted_A.csv"), sep=",")

        return True

    def plot_charts(self):
        """"""
        self.dfA = pd.read_csv(Path.joinpath(self.root, "corpus", "plotted_A.csv"))

        csv_files = glob.glob(Path.joinpath(self.root, f"*.csv").as_posix())
        # print(csv_files)
        # with open(csv_files[0], "r") as f:
        #     print(f.read())
        self.dfB = pd.read_csv(csv_files[0])


        print(self.dfA.head())
        self.dfB.rename(columns={'Total': 'TotalB'}, inplace=True)
        print(self.dfB.head())

        df = pd.merge_asof(self.dfA, self.dfB, on='Time')
        df.plot(x="Time", y=["Total", "TotalB"])
        plt.show()

    def compare_dataframes(self):
        """"""
        dfA = pd.read_csv(Path.joinpath(self.root, "corpus", "plotted_A.csv"))
        dfB = pd.read_csv(Path.joinpath(self.root, "plotted_A.csv"))
        dfB.columns = self.dfB.columns.str.replace('Total', 'TotalB')

        head_count = min([len(dfA), len(dfB)])

        dfA = dfA.head(head_count)
        dfB = dfB.head(head_count)

        del dfA['Time']
        del dfB['Time']
        del dfA['Total']
        del dfB['TotalB']

        print(dfA.compare(dfB))


if __name__ == "__main__":
    print("STARTING UP ---- new branch ...")
    # Benchmark().one_percent_sample()

    benchmark = Benchmark()

    benchmark.unzip()
    benchmark.plot_charts()
    benchmark.compare_dataframes()

    # csv_files = glob.glob(Path.joinpath(benchmark.root, "corpus", f"*.csv").as_posix())
    # print(csv_files, "BEFORE")
    # if "/home/runner/work/pingme/pingme/corpus/plotted_A.csv" not in csv_files:
    #     benchmark.file_append = "A"
    # else:
    #     benchmark.file_append = "B"
    #
    # benchmark.unzip()
    # csv_files = glob.glob(Path.joinpath(benchmark.root, "corpus", f"*.csv").as_posix())
    # print(csv_files, "NOW... and later")

    # Upload and save the plotted values ... here...
    # import os
    # if os.path.exists("/home/runner/work/pingme/pingme/corpus/plotted_B.csv"):
    #     print("Running the Final Charts")
    #     Benchmark().plot_charts()
    #     Benchmark().compare_dataframes()
    #     print("SHUTTING DOWN ---- new branch")
    # else:
    #     print("NO PLOTTED B?????")