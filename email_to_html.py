"""
Class for converting emails to HTML
"""
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

    def email_to_object(self):

        # Open email file for reading as binary and parse it into an email object
        try:
            with open(self.email_file, 'rb') as email_file:
                email_msg: object = BytesParser(policy=policy.default).parse(email_file)
                self.msg: object = email_msg
        except Exception as error:
            logger.error(f"Error when opening file {email_file}. Error:\n{error}")
            self.msg = None

    def is_msg_multipart(self) -> bool:
        if self.msg:
            return self.msg.is_multipart()

    def email_file_to_html(self):

        # Open email file for reading as binary and parse it into an email object
        # with open(self.email_file, 'rb') as email_file:
        #     email_msg: object = BytesParser(policy=policy.default).parse(email_file)
        email_msg = self.msg
        # Get attributes from email
        self.email_from: str = email_msg["from"]
        self.email_to: str = email_msg["to"]
        self.email_subject: str = email_msg["subject"]
        self.email_date: str = email_msg["date"]

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

        return email_body_content





# m = EmailToHtml("/home/i/git/email_to_pdf/email.eml")
# m_r = m.email_to_object()
# m_m = m.is_msg_multipart()
# import pdb; pdb.set_trace()
