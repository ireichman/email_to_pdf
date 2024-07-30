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
    parser.add_argument("-s", "--source", required=True, nargs="+", help="Coma separated list of eml files.")
    parser.add_argument("-o", "--output", required=True, type=str, nargs=1, help="list of output paths, "
                                                                                   "if different from the working path. ")

    parser.add_argument("-on", "--output_name", type=str, nargs=1, help="Pattern to use for file name. "
                                                                        "The output file will be added a number if more"
                                                                        "then one file is processed. If no name is "
                                                                        "given, the email's file name will be used.")

    return parser.parse_args()
