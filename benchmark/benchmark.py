# flake8: noqa: E402
import argparse
import bz2
import csv
import datetime
import os
import re
import sys
from ast import literal_eval as to_list
from io import StringIO
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from eyecite import get_citations

csv.field_size_limit(sys.maxsize)

root = Path(__file__).parent.absolute()

MAX_ROWS_IN_MD = 51


class Benchmark(object):
    """Benchmark the different eyecite branches"""

    def __init__(self):
        self.now = datetime.datetime.now()
        self.times = []
        self.totals = []
        self.list_of_ids = []
        self.opinions = []
        self.count = 0
        self.fields = []
        self.gains = []
        self.losses = []

    def get_filepath(self, filename):
        return Path.joinpath(root, filename)

    def fetch_citations(self, row) -> None:
        """Fetch citations from rows opinion data

        return: None
        """
        row_id = row[0]
        row = dict(zip(self.fields, row))
        # Find opinions to test against from the zip file and return
        # citations found
        non_empty_rows = [
            row[field] for field in self.fields if type(row[field]) == str
        ]
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

    def generate_branch_report(self, branch: str) -> None:
        """Generate Report

        :param branch: Is a branch from main or not
        :return: None
        """
        zipfile = bz2.BZ2File(self.get_filepath("bulk-file.csv.bz2"))
        csv_data = csv.reader(StringIO(zipfile.read().decode()), delimiter=",")
        self.fields = next(csv_data)
        for row in csv_data:
            self.fetch_citations(row)

        df = pd.DataFrame(
            {
                "OpinionID": self.list_of_ids,
                "Time": self.times,
                "Total": self.totals,
                "Opinions": self.opinions,
            }
        )
        df.to_csv(index=False, path_or_buf=self.get_filepath(f"{branch}.csv"))

    def compare_dataframes(self, main_hash: str, branch_hash: str) -> None:
        """Compare generated data frames between branches

        Generates (mostly) the markdown report for the PR comment

        Returns: None
        """
        main = pd.read_csv(
            self.get_filepath(f"{main_hash}.csv"),
            usecols=["OpinionID", "Opinions"],
        )
        branch = pd.read_csv(
            self.get_filepath(f"{branch_hash}.csv"),
            usecols=["OpinionID", "Opinions"],
        )

        comparison = main.compare(branch)

        with open(self.get_filepath("output.csv"), "w") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "GAIN", "LOSS", "OPINION_ID", "--"])

            for row in comparison.iterrows():
                if row[1][0] == row[1][1]:
                    continue
                # Convert str list of citations back to list to compare across
                # branches
                non_overlap = set(to_list(row[1][0])) ^ set(to_list(row[1][1]))
                if len(list(non_overlap)) == 0:
                    continue

                for item in list(non_overlap):
                    if item in list(row[1][0]):
                        self.gains.append(item)
                        row_to_add = [row[0], item, "", main.iat[row[0], 0]]
                    else:
                        self.losses.append(item)
                        row_to_add = [row[0], "", item, branch.iat[row[0], 0]]
                    writer.writerow(row_to_add)

    def write_report(self):
        """Begin building Report.MD file

        :return: None
        """
        with open(self.get_filepath("report.md"), "w") as f:
            f.write("# The Eyecite Report :eye:\n\n")
            f.write("\n\nGains and Losses\n")
            f.write("---------\n")
            f.write(
                f"There were {len(self.gains)} gains and "
                f"{len(self.losses)} losses.\n"
            )
            f.write("\n<details>\n")
            f.write("<summary>Click here to see details.</summary>\n\n")

        # Add markdown report file outputs
        df = pd.read_csv(self.get_filepath("output.csv"))

        with open(self.get_filepath("report.md"), "a") as md:
            if df.__len__() > MAX_ROWS_IN_MD:
                with open("report.md", "a+") as f:
                    f.write(
                        f"There were {df.__len__()} changes so we are only "
                        f"displaying the first 50. You can review the \n"
                        f"entire list by downloading the output.csv "
                        f"file linked above.\n\n"
                    )

                df[:MAX_ROWS_IN_MD].to_markdown(buf=md)
            else:
                df.to_markdown(buf=md)

        # Remove NAN from file to make it look cleaner
        with open(self.get_filepath("report.md"), "r+") as f:
            file = f.read()
            file = re.sub("nan", "   ", file)
            f.seek(0)
            f.write(file)
            f.truncate()

        with open(self.get_filepath("report.md"), "a+") as f:
            f.write("\n\n</details>\n")

        # Add header for time chart for PR comment
        with open(self.get_filepath("report.md"), "a") as f:
            f.write("\n\nTime Chart\n")
            f.write("---------\n")

    def generate_time_chart(self, main, branch) -> None:
        """Generate time chart showing speed across branches

        return: None
        """
        main = pd.read_csv(self.get_filepath(f"{main}.csv"))
        branch = pd.read_csv(self.get_filepath(f"{branch}.csv"))

        main.columns = main.columns.str.replace("Total", "Total Main")
        branch.columns = branch.columns.str.replace("Total", "Total Branch")

        df = pd.merge_asof(main, branch, on="Time")
        df.plot(kind="line", x="Time", y=["Total Main", "Total Branch"])

        plt.ylabel("# Cites Found ", rotation="vertical")
        plt.savefig(self.get_filepath("chart.png"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chart", action="store_true")
    parser.add_argument("--main")
    parser.add_argument("--branch")

    args = parser.parse_args()
    branch = args.branch
    main = args.main

    benchmark = Benchmark()
    if args.chart:
        # Process the report
        benchmark.compare_dataframes(main, branch)

        # Write Report.MD file
        benchmark.write_report()

        # Generate time chart
        benchmark.generate_time_chart(main, branch)
    else:
        # Generate data comparison
        version = main if main else branch
        benchmark.generate_branch_report(branch=version)
