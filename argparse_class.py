"""
Handling command line args.
"""
import argparse

usage = ""
parser = argparse.ArgumentParser(prog="Email2PDF", usage="", add_help=True)
parser.add_argument("-s", "--source", type=str, nargs="?", help="")
parser.add_argument("-o", "--output", type=str, nargs=1, help="")
parser.add_argument("-on", "--output_name", type=str, nargs=1, help="")

args = parser.parse_args()
