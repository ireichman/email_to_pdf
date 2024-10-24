"""
Class for converting emails to HTML
"""
import sys
from base64 import decode
from email.parser import BytesParser
from email import policy
from loguru import logger


class EmailToHtml:
    """
    Using 'email' library to convert eml files to HTML
    """
    def __init__(self, email_file: str):
        self.email_file: str = email_file
        self.email_from: str = ""
        self.email_to: str = ""
        self.email_subject: str = ""
        self.email_date: str = ""
        self.msg: object = None
        self.msg_is_multipart: bool = False

    def email_file_to_object(self):

        # Open email file for reading as binary and parse it into an email object
        try:
            with open(self.email_file, 'rb') as email_file:
                email_msg: object = BytesParser(policy=policy.default).parse(email_file)
                self.msg: object = email_msg
        except Exception as error:
            logger.error(f"Error when opening file {email_file}. Error:\n{error}")
            self.msg = None

    def is_msg_multipart(self):

        logger.info(f"Checking if email is multipart with files.")
        if self.msg:
            if self.msg.is_multipart():
                if self.msg.get_content_subtype() == "related":
                    logger.info(f"Email is multipart/ related.")
                    return True
                else:
                    return False
            else:
                return False

    def msg_object_to_html(self):

        # Open email file for reading as binary and parse it into an email object
        # with open(self.email_file, 'rb') as email_file:
        #     email_msg: object = BytesParser(policy=policy.default).parse(email_file)
        email_msg = self.msg
        # Get attributes from email
        self.email_from: str = email_msg["from"]
        self.email_to: str = email_msg["to"]
        self.email_subject: str = email_msg["subject"]
        self.email_date: str = email_msg["date"]

        # Checking if email is multipart.
        if self.is_msg_multipart():
            logger.info(f"{self.email_file} is multipart/ related")
            email_body_content = self.multipart_with_files_parser()
        else:
        # Get the body of the email message.
            try:
                email_body = email_msg.get_body()
            except Exception as error:
                logger.error(f"Error while getting email body. Error:\n{error}")

            # Get the HTML content of the email's body element.
            try:
                email_body_content = email_body.get_content()
            except Exception as error:
                logger.error(f"Error while getting email body's content. Error:\n{error}")
        email_body_content = email_body_content or ""
        return email_body_content

    def multipart_with_files_parser(self):

        # variables for html and email files.
        html_part: str = ""
        related_parts: set = {}

        # Getting all the parts of the multipart email.
        try:
            email_parts: object = self.msg.iter_parts()
            logger.debug(f"Parts in {self.email_file}:\n{email_parts}")
        except Exception as error:
            logger.error(f"Error getting parts from {self.email_file}. Error:\n{error}")
            sys.exit(1)

        for part in email_parts:
            logger.debug(f"Processing {self.email_file} part {part}")
            content_type = part.get_content_type()
            if content_type == "text/html":
                html_part = part.get_payload(decode=True).decode(part.get_content_charset())
            elif content_type.startswith('image/'):
                # Extract images and add them to related_parts var
                cid = part["Content-ID"]
                if cid:
                    cid = cid.strip("<>")
                    related_parts[cid] = part

        # Replace cid reference with actual inline image.
        for cid, part in related_parts.items():
            # Decode the email part.
            part_data = part.get_payload(decode=True)
            # save the email part
            part_file_name = part.get_filename() or f"{cid}.png"
            with open(f"tmp/{part_file_name}", 'wb') as part_file:
                part_file.write(part_data)
            html_content = html_part.replace(f"cid:{cid}", f"tmp/{part_file_name}")
        return html_content




# m = EmailToHtml("/home/i/git/email_to_pdf/email.eml")
# m_r = m.email_to_object()
# m_m = m.is_msg_multipart()
# import pdb; pdb.set_trace()
