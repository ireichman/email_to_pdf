from loguru import logger
import os
from pathlib import Path
from email_to_html import EmailToHtml


def find_working_directory() -> str:
    """
    Used for finding the current working directory.
    :return: String with absolute path to working directory.
    """
    current_dir = os.getcwd()
    return current_dir


def delete_all_temp_files():
    """
    Used to empty the 'tmp' directory.
    :return: Nothing.
    """
    folder_path = find_working_directory() + "/tmp/"
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as error:
            logger.error(f"Error deleting temporary files. Error:\n{error}")


def parse_email(mail_file: str) -> dict:

    logger.info(f"Parsing {mail_file}")
    email = EmailToHtml(email_file=mail_file)
    email.email_file_to_object()
    email_parsed = email.msg_object_to_html()
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
        logger.debug(f"Removing file extension.")
        name: str = naming_pattern[0].split(".")[0]
    else:
        # Remove the file path and  extension.
        email_file_parts = Path(email_name)
        name: str = email_file_parts.stem #email_name.split("/")[-1].split(".")[0]

    if output_path:
        logger.debug(f"Adding user's path ({output_path}) to name ({name}).")
        name: str = output_path + name
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
