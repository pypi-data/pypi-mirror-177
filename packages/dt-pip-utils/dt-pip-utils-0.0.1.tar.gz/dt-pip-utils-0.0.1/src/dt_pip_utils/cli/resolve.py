#!/usr/bin/env python3

import argparse

from ..update import update_versions


def resolve():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="Input dependencies file"
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=False,
        help="Output (resolved) dependencies file"
    )

    parsed = parser.parse_args()

    update_versions(fin=parsed.input, fout=parsed.output)


if __name__ == '__main__':
    resolve()
