import mailparser
from weasyprint import HTML as html2pdf
from loguru import logger
import os
from argparse_class import get_args


def parse_mail(mail: str) -> dict:
    """
    Parse emails for data.
    :param mail: location of an email file as a string.
    :return: a dictionary with information from the email. Including the body of the email.
    """
    # Parse eml
    logger.info(f"Parsing email from string {mail}")
    try:
        mail = mailparser.parse_from_file(mail)
    except Exception as error:
        logger.error(f"Failed to parse email with error\n{error}")

    # Find info in email object.
    subject = mail.subject
    date = mail.date
    body = mail.body
    body_html_only = body.split("<head>")[1]
    body_html_only_fixed = "<head>" + body_html_only
    email_data = {"subject": subject, "date": date, "body": body_html_only_fixed}
    logger.info(f"email was parsed successfully. Email info:\n{email_data}")
    return email_data


def check_file_or_path_exists(file_or_path: str) -> bool:
    """
    Checks if a file exists and is of the right format.
    :param file_or_path: A string which is a path of a file with path.
    :return: Boolean.
    """
    # Check that file exists.
    if not os.path.exists(file_or_path):
        logger.error(f"Could not find {file_or_path}")
        return False
    else:
        return True

# def check_file_extension(file_with_path: str) -> bool:
#     # Find the file's extension.
#     try:
#         file_extension = file_with_path.split(".")[1]
#     except Exception as error:
#         logger.error(f"Could not find file's extension. Error:\n{error}")
#
#     if
#     # Add file validation?
#     return {"file_exists": True, "message": f"{file_extension}"}


def convert_to_pdf(html_string: str, output, output_naming_template: str) -> bool:

    pass
if __name__ == "__main__":
    print("Starting program...")

args = get_args()

# Compile a list of files to convert and check if they exist in the OS.
if args.source:
    logger.info(f"Argument received from source parameter: {args.source}")
    list_of_emails: list = args.source
    logger.info(f"Files to convert to PDF:\n{list_of_emails}")
    # Checking that the email files exist in the OS.
    list_of_emails_validated = filter(check_file_or_path_exists, list_of_emails)
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
    output_path: str = args.output
    # Check if path exist in the system.
    path_validated = check_file_or_path_exists(output_path)
    if not path_validated:
        print(f"Path does not exist: {output_path}")
        exit()

if args.output_name:
    logger.info(f"Argument received from output_name parameter: {args.output_name}")
    output_file_name: str = args.output_name

# Parsing the emails and makes a list of strings. Each string is an HTML.
list_of_emails_parsed = map(parse_mail, list_of_emails_validated)

# print(f"{mail["subject"]}\n{mail["date"]}\n{mail["body"]}")

# html2pdf(string=mail["body"]).write_pdf("pdf.pdf")

import pdb; pdb.set_trace()
