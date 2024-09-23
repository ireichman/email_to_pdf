"""
Class for converting emails to HTML
"""
from email.parser import BytesParser
from email import policy


class EmailToHtml:
    """

    """
    def __init__(self, email_file: str):
        self.email_file: str = email_file
        self.email_from: str = ""
        self.email_to: str = ""
        self.email_subject: str = ""
        self.email_date: str = ""

    def email_file_to_html(self):

        # Open email file for reading as binary and parse it into an email object
        with open(self.email_file, 'rb') as email_file:
            email_msg: object = BytesParser(policy=policy.default).parse(email_file)

        # Get attributes from email
        self.email_from: str = email_msg["from"]
        self.email_to: str = email_msg["to"]
        self.email_subject: str = email_msg["subject"]
        self.email_date: str = email_msg["date"]

        # Get the body of the email message.
        email_body = email_msg.get_body()
        return email_body.get_content()


# m = EmailToHtml("/home/i/git/email_to_pdf/email.eml")
# m_2_h = m.email_file_to_html()
#
# a = 1
