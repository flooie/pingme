import argparse
from ast import literal_eval as to_list
import csv
import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

csv.field_size_limit(sys.maxsize)

root = Path(__file__).parent.absolute()
fp_main = Path.joinpath(root, "outputs", f"main.csv")
fp_branch = Path.joinpath(root, "outputs", f"branch.csv")


def compare_dataframes() -> None:
    """Compare generated data frames between branches

    Generates (mostly) the markdown report for the PR comment

    Returns: None
    """
    gains = []
    losses = []
    main = pd.read_csv(fp_main, usecols=["OpinionID", "Opinions"])
    branch = pd.read_csv(fp_branch, usecols=["OpinionID", "Opinions"])

    comparison = main.compare(branch)

    with open("outputs/output.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "GAIN", "LOSS", "OPINION_ID", "--"])

        for row in comparison.iterrows():
            if row[1][0] == row[1][1]:
                continue

            non_overlap = set(to_list(row[1][0])) ^ set(to_list(row[1][1]))
            if len(list(non_overlap)) == 0:
                continue

            for item in list(non_overlap):
                if item in list(row[1][0]):
                    gains.append(item)
                    row_to_add = [row[0], item, "", main.iat[row[0], 0]]
                else:
                    losses.append(item)
                    row_to_add = [row[0], "", item, branch.iat[row[0], 0]]
                writer.writerow(row_to_add)

    # Generate our report based on the provided information.
    with open("outputs/report.md", "w") as f:
        f.write("# The Eyecite Report :eye:\n")
        f.write("")
        f.write(f"There were {len(gains)} gains and {len(losses)} losses.\n")
        f.write("You can verify any losses by using the cluster id generated\n")
        f.write("# Output\n")
        f.write("---------\n\n")
        f.write(
            "The following chart illustrates the gains and losses "
            "(if any) from the current pr.\n"
        )

        f.write("<details>")

    # Add markdown report file outputs
    df = pd.read_csv("outputs/output.csv")

    with open("outputs/report.md", "a") as md:
        if df.__len__() > 51:
            with open("outputs/report.md", "a+") as f:
                f.write(
                    f"There were {df.__len__()} changes so we are only "
                    f"displaying the first 50. You can review the \n"
                    f"entire list by downloading the output.csv "
                    f"file linked above.\n\n"
                )

            df[:51].to_markdown(buf=md)
        else:
            df.to_markdown(buf=md)

    # Remove NAN from file to make it look cleaner
    with open("outputs/report.md", "r+") as f:
        file = f.read()
        file = re.sub("nan", "   ", file)
        f.seek(0)
        f.write(file)
        f.truncate()
        f.write("</details>")

    # Add header for time chart for PR comment
    with open("outputs/report.md", "a") as f:
        f.write("\n\n# Speed Comparison\n### Main Branch vs. PR Branch\n")


def generate_time_chart() -> None:
    """Generate time chart showing speed across branches

    return: None
    """

    main = pd.read_csv(fp_main)
    branch = pd.read_csv(fp_branch)

    main.columns = main.columns.str.replace("Total", f"Total Main")
    branch.columns = branch.columns.str.replace("Total", f"Total Branch")
    df = pd.merge_asof(main, branch, on="Time")

    df.plot(kind="line", x="Time", y=[f"Total Main", f"Total Branch"])
    plt.ylabel("# Cites Found ", rotation="vertical")

    plt.savefig("outputs/time-comparison.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A tool to generate benchmarks in eyecite."
    )

    # Process the report
    compare_dataframes()
    # Generate time chart
    generate_time_chart()
