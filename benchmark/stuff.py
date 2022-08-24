"""Hello world"""
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--something")
    args = parser.parse_args()

    print(args.something)
    print("Hello Check Me Branch --- decidedly not main")
    print("And more.")