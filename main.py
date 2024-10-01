
from pdfkit import PDFKit
from loguru import logger
import os
from pathlib import Path
from argparse_funct import get_args
from email_to_html import EmailToHtml
from html_to_pdf import HtmlToPdf

def parse_email(mail_file: str) -> dict:

    email = EmailToHtml(email_file=mail_file)
    email_parsed = email.email_file_to_html()
    email_data = {"email_file": mail_file, "subject": email.email_subject, "date": email.email_date,
                  "body": email_parsed}
    return email_data

def check_file_or_path_exists(file_or_path: str) -> bool:
    """
    Checks if a file exists and is of the right format.
    :param file_or_path: A string which is a path of a file with path.
    :return: Boolean.
    """
    logger.info(f"Checking if {file_or_path} exists in the OS' file system.")
    # Check that file exists.
    if not os.path.exists(file_or_path):
        logger.info(f"Could not find {file_or_path}")
        return False
    else:
        logger.info(f"Found {file_or_path} in the OS' file system.")
        return True

def pdf_naming(naming_pattern: str = None, output_path: str = None, email_name: str = None):

    logger.info(f"Naming the PDF using naming_pattern: {naming_pattern}, output_path: {output_path} and email_name: "
                f"{email_name}")
    if naming_pattern:
        # Remove the file extension, if exists.
        name: str = naming_pattern[0].split(".")[0]
    else:
        # Remove the file path and  extension.
        email_file_parts = Path(email_name)
        name: str = email_file_parts.stem #email_name.split("/")[-1].split(".")[0]

    if output_path:
        name = output_path + name
        path: str = output_path

    # Testing if file already exists and renaming if it does.
    while check_file_or_path_exists(name + ".pdf"):
        logger.info(f"Found that file {name + ".pdf"} already exists")
        name_split_by_dash = name.rsplit(sep="-", maxsplit=1)
        logger.debug(f"Split {name} to {name_split_by_dash}")
        try:
            serial_number_for_file_ending = name_split_by_dash[-1]
            name = name_split_by_dash[0]
            # Checking if the file ends with a number
            int(serial_number_for_file_ending)
        except Exception as error:
            logger.error(f"Error when parsing file name: {error}")
            serial_number_for_file_ending = 0
        name = name + f"-{int(serial_number_for_file_ending) + 1}"

        if int(serial_number_for_file_ending) >= 100:
            logger.critical(f"100 or more instances of file {name + ".pdf"} already exist.")

    else:
        pdf_name = name

    pdf_name = pdf_name + ".pdf"
    return pdf_name


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

# TODO: Add option for overwriting files???
# TODO: Add option to print multiple emails to 1 pdf.
# TODO: Add ability to get date from email (both metadata and text) for use with file name.
# TODO: Add verbosity.

# Convert HTML string from parsed email to PDF.
for email in list_of_emails_parsed:
    pdf_name = pdf_naming(naming_pattern=output_file_name, output_path=path_validated, email_name=email["email_file"])
    pdf_o = PDFKit(url_or_file=email["body"], type_="string", verbose=True)
    pdf_o.to_pdf(path=pdf_name)
    logger.success(f"Converted {email["email_file"]} to {pdf_name} successfully.")
    print(f"Converted {email["email_file"]} to {pdf_name} successfully.")

