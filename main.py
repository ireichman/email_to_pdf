
from pdfkit import PDFKit
from loguru import logger
from argparse_funct import get_args
from utils import pdf_naming, parse_email, check_file_or_path_exists

# TODO: Add option for overwriting files???
# TODO: Add option to print multiple emails to 1 pdf.
# TODO: Add ability to get date from email (both metadata and text) for use with file name.
# TODO: Add verbosity to argparse. Hide all logging messages unless logging is True.

if __name__ == "__main__":
    args = get_args()
    print("Starting program...")

# Compile a list of files to convert and check if they exist in the OS.
if args.source:
    logger.info(f"Argument received from source parameter: {args.source}")
    list_of_emails: list = args.source
    logger.info(f"Files to convert to PDF:\n{list_of_emails}")
    # Checking that the email files exist in the OS.
    list_of_emails_validated = list(filter(check_file_or_path_exists, list_of_emails))
    # Comparing the list of emails from argparse and the subsection of the same files that exist in the OS.
    files_not_in_the_os = list(set(list_of_emails) ^ set(list_of_emails_validated))
    logger.info(f"Files that are not found in the OS: {files_not_in_the_os}")
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
    path_validated = ""

if args.output_name:
    logger.info(f"Argument received from output_name parameter: {args.output_name}")
    output_file_name: str = args.output_name
else:
    output_file_name = ""

# Parsing the emails and makes a list of strings. Each string is an HTML.
list_of_emails_parsed = map(parse_email, list_of_emails_validated)
logger.info(f"Parsed the list of email.")

# Convert HTML string from parsed email to PDF.
for email in list_of_emails_parsed:
    pdf_name = pdf_naming(naming_pattern=output_file_name, output_path=path_validated, email_name=email["email_file"])
    pdf_o = PDFKit(url_or_file=email["body"], type_="string", verbose=True)
    pdf_o.to_pdf(path=pdf_name)
    logger.success(f"Converted {email["email_file"]} to {pdf_name} successfully.")
    print(f"Converted {email["email_file"]} to {pdf_name} successfully.")

print(f"Finished converting {len(args.source)} emails to PDFs")