
import argparse
import ast
from pathlib import Path
import csv
import sys

csv.field_size_limit(sys.maxsize)

import pandas as pd
import matplotlib.pyplot as plt


class Benchmark(object):
    """"""

    def __init__(self):
        """"""
        self.root = Path(__file__).parent.absolute()
        self.dfa = None
        self.dfb = None
        self.branch1 = None
        self.branch2 = None


    def compare_dataframes(self):
        """"""
        ids = []
        gains = []
        losses = []
        dfA = pd.read_csv(Path.joinpath(self.root, "outputs", f"plotted-{self.branch1}.csv"))
        dfB = pd.read_csv(Path.joinpath(self.root, "outputs", f"plotted-{self.branch2}.csv"))

        head_count = min([len(dfA), len(dfB)])

        dfA = dfA.head(head_count)
        dfB = dfB.head(head_count)

        del dfA['Time']
        del dfB['Time']
        del dfA['Total']
        del dfB['Total']
        print("Ok")
        comparison = dfA.compare(dfB)

        with open("outputs/output.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(['ID', "GAIN", "LOSS", "OPINION_ID"])
            for row in comparison.iterrows():
                non_overlap = set(ast.literal_eval(row[1][0])) ^ set(ast.literal_eval(row[1][1]))
                if len(list(non_overlap)) == 0:
                    continue
                for item in list(non_overlap):
                    if item in list(ast.literal_eval(row[1][0])):
                        gains.append(item)
                        row_to_add = [row[0], item, "", dfA.iat[row[0],0]]
                    else:
                        losses.append(item)
                        row_to_add = [row[0], "", item, dfA.iat[row[0],0]]
                    writer.writerow(row_to_add)

        # Generate our report based on the provided information.
        with open("outputs/report.md", "w") as f:
            f.write("The output here was most likely good.\n")
            f.write(f"There were {len(gains)} gains and {len(losses)} losses.\n")
            f.write(f"You can verify any losses by using the cluster id generated\n")
            f.write(f"With the following IDs... oh great. None.\n")

    def generate_report(self):
        """"""
        dfA = pd.read_csv(Path.joinpath(self.root, "outputs", f"plotted-{self.branch1}.csv"))
        dfB = pd.read_csv(Path.joinpath(self.root, "outputs", f"plotted-{self.branch2}.csv"))

        dfA.columns = dfA.columns.str.replace('Total', f'Total {self.branch1}')
        dfB.columns = dfB.columns.str.replace('Total', f'Total {self.branch2}')
        df = pd.merge_asof(dfA, dfB, on='Time')

        df.plot(x="Time", y=[f'Total {self.branch1}', f'Total {self.branch2}'])
        plt.savefig('outputs/time-comparison.png')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A test program.')
    parser.add_argument('--branch1')
    parser.add_argument('--branch2')
    args = parser.parse_args()

    benchmark = Benchmark()
    benchmark.branch1 = args.branch1
    benchmark.branch2 = args.branch2
    benchmark.compare_dataframes()
    benchmark.generate_report()

