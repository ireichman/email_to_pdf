"""
Class for converting HTML to PDF.
"""
import pdfkit
from loguru import logger


class HtmlToPdf:
    """
    Wrapper for pdfkit. Pdfkit requires wkhtmltopdf installed. I hope to replace pdfkit once I find another open-source
    library that works well. Not all of pdfkit options are available yet.
    """
    def __init__(self, html_data: str, output_file_name_and_path: str, verbosity: bool = None, css: list = None):
        """
        
        :param html_data: Depending on the 'input_format' it can be: String of HTML code / file path/ URL path.
        :param output_file_name_and_path: String with relative or absolute path and name of output file.
        :param verbosity: True turns wkhtmltopdf verbosity on. False disable verbosity.
        :param css: List with paths to CSS files. Ignored if list is empty / None.
        """

        self.html_data: str = html_data
        self.output: str = output_file_name_and_path
        self.verbosity: bool = verbosity
        self.css: list = css

    def create_pdf_from_string(self):
        """"""
        logger.info(f"Starting HTML to PDF conversion with output: {self.output}")
        try:
            pdfkit.from_string(input=self.html_data, output_path=self.output, verbose=self.verbosity, css=self.css)
        except Exception as error:
            logger.error(f"Error while converting HTML to PDF. \n{error}")
            return False
        return True