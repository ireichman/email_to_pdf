import sys

from pdfkit import PDFKit
from loguru import logger
from argparse_funct import get_args
from utils import pdf_naming, parse_email, check_file_or_path_exists, delete_all_temp_files

# TODO: Add option for overwriting files???
# TODO: Add option to print multiple emails to 1 pdf.
# TODO: Add ability to get date from email (both metadata and text) for use with file name.
# TODO: Check for name split by '_' not just '-'. Change default naming to under score.
# TODO: Does PDF has to have a page size or can it just be unlimited? (So it does not cut email).

if __name__ == "__main__":
    args = get_args()
    print("-" * 50)
    print("Starting Email to PDF...")
    print("-" * 50)

logger.remove()
if args.verbose:
    print("Verbose messaging enabled.")
    logger.add(sink=sys.stderr, level="DEBUG")

# Compile a list of files to convert and check if they exist in the OS.
if args.source:
    logger.info(f"Argument received from source parameter: {args.source}")
    list_of_emails: list = args.source
    logger.info(f"Files to convert to PDF:\n{list_of_emails}")
    # Checking that the email files exist in the OS.
    list_of_emails_validated = list(filter(check_file_or_path_exists, list_of_emails))
    print(f"Found the following email files:\n{list_of_emails_validated}")
    # Comparing the list of emails from argparse and the subsection of the same files that exist in the OS.
    files_not_in_the_os = list(set(list_of_emails) ^ set(list_of_emails_validated))
    logger.info(f"Files that are not found in the OS: {files_not_in_the_os}")
    if files_not_in_the_os:
        print(f"The following files were not found on your system:\n{files_not_in_the_os}")
    if not list_of_emails_validated:
        print("Files were not found on the system.\nExiting...")
        exit()

# Check that args.output gives a real path.
if args.output:
    logger.info(f"Argument received from output parameter: {args.output}")
    output_path: str = args.output[0]
    # Check if path exist in the system.
    path_validated = check_file_or_path_exists(output_path)
    if not path_validated:
        print(f"Path does not exist: {output_path}. Please provide a valid path with -o or --output option."
              f"\nAlternatively you could not specify this option to save in the same directory you run it from.")
        exit()
else:
    output_path = ""

if args.output_name:
    logger.info(f"Argument received from output_name parameter: {args.output_name}")
    output_file_name: str = args.output_name
else:
    output_file_name = ""

# Parsing the emails and makes a list of strings. Each string is an HTML.
list_of_emails_parsed = map(parse_email, list_of_emails_validated)
logger.info(f"Parsed the list of emails.")

# Convert HTML string from parsed email to PDF.
for email in list_of_emails_parsed:
    print(f"Processing {email["email_file"]}")
    # Choosing a name for the output PDF
    pdf_name = pdf_naming(naming_pattern=output_file_name, output_path=output_path, email_name=email["email_file"])
    logger.info(f"PDF name: {pdf_name}")
    # Creating PDF object.
    logger.info(f"Starting conversion to {pdf_name}")
    pdf_o = PDFKit(url_or_file=email["body"], type_="string", verbose=args.verbose, options={"enable-local-file-access": True})
    pdf_o.to_pdf(path=pdf_name)
    logger.success(f"Converted {email["email_file"]} to {pdf_name} successfully.")
    print(f"Converted {email["email_file"]} to {pdf_name} successfully.")

# Delete all temp files and folders created in this session.
delete_all_temp_files()

print(f"Finished converting {len(args.source)} emails to PDFs.")