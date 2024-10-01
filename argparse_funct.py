"""
Handling command line args.
"""
import argparse

usage = """To run this program, wkhtmltopdf needs to be installed on the system. 
            Run this program with python main.py -s <path-to_email> -o <path/and/name/for_output_file.pdf> """
def get_args():
    """
    Parse command line arguments.
    :return: Return parsed args.
    """
    usage = ("Run tha application using `python main.py -source <file1.eml file2.eml>` This will convert the emails while"
             " keeping their file names.")

    parser = argparse.ArgumentParser(prog="Email2PDF", usage="", add_help=True, description="")
    parser.add_argument("-s", "--source", required=True, nargs="+", help="Coma separated list of eml files.")
    parser.add_argument("-o", "--output", required=False, type=str, nargs=1, help="Specify an output path, "
                                                                                   "if different from the working path.")

    parser.add_argument("-on", "--output_name", type=str, nargs=1, help="Pattern to use for file name. "
                                                                        "The output file will be added a number if more"
                                                                        " then one file is processed. If no name is "
                                                                        "given, the email's file name will be used.")

    return parser.parse_args()
