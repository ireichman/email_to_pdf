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


def check_file(file_with_path: str) -> dict:
    """
    Checks if a file exists and is of the right format.
    :param file: the location of a file in the OS.
    :return: Boolean.
    """
    # Check that file exists.
    if not os.path.exists(file_with_path):
        logger.error(f"Could not find {file_with_path}")
        return {"file_exists": False, "message": "File does not exist."}
    # Find the file's extension.
    file_extension = file_with_path.split(".")[1]
    # Add file validation?
    return {"file_exists": True, "message": f"{file_extension}"}


def convert_to_pdf(html_string: str, output output_naming_template: str) ->
if __name__ == "__main__":
    print("Starting program...")

args = get_args()

if args.source:
     check_file()
# mail = parse_mail("email.eml")

print(f"{mail["subject"]}\n{mail["date"]}\n{mail["body"]}")

html2pdf(string=mail["body"]).write_pdf("pdf.pdf")

