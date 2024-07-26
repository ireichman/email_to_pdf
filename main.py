import mailparser
from weasyprint import HTML as html2pdf
from argparse_class import parser
from loguru import logger

def parse_mail(mail: str):
    # Parse eml
    mail = mailparser.parse_from_file(mail)

    # Find info in eml
    subject = mail.subject
    date = mail.date
    body = mail.body
    body_html_only = body.split("<head>")[1]
    body_html_only_fixed = "<head>" + body_html_only
    return {"subject": subject, "date": date, "body": body_html_only_fixed}





if __name__ == "__main__":
    print("Starting program...")

mail = parse_mail("email.eml")

print(f"{mail["subject"]}\n{mail["date"]}\n{mail["body"]}")

html2pdf(string=mail["body"]).write_pdf("pdf.pdf")
"restructure"

