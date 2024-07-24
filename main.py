import mailparser
from weasyprint import HTML as html2pdf
# Parse eml
mail = mailparser.parse_from_file("email.eml")

# Find info in eml
subject = mail.subject
date = mail.date
body = mail.body
body_html_only = body.split("<head>")[1]
body_html_only_fixed = "<head>" + body_html_only

print(f"{subject}\n{date}\n{body_html_only_fixed}")

html2pdf(string=body_html_only).write_pdf("pdf.pdf")
