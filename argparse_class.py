"""
Handling command line args.
"""
import argparse

def get_args():
    """
    Parse command line arguments.
    :return: Return parsed args.
    """
    usage = ""
    parser = argparse.ArgumentParser(prog="Email2PDF", usage="", add_help=True)
    parser.add_argument("-s", "--source", type=str, nargs="?", help="Coma seperated list of eml files.")
    parser.add_argument("-o", "--output", type=str, nargs=1, help="An output path, if different from the "
                                                                  "working path.")
    parser.add_argument("-on", "--output_name", type=str, nargs=1, help="Pattern to use for file name. "
                                                                        "The output file will be added a number if more"
                                                                        "then one file is processed.")

    return parser.parse_args()
