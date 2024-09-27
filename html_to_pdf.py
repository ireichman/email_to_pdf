"""
Class for converting HTML to PDF.
"""
import pdfkit
from loguru import logger


class HtmlToPdf:

    def __init__(self, html_data: str, output_file_name_and_path: str, input_format: str = "file",
                 verbosity: bool = None, css: list = None):

        self.html_data: str = html_data
        self.output: str = output_file_name_and_path
        self.input_format: str = input_format
        self.verbosity: bool = verbosity
        self.css: list = css

    def create_pdf(self):

        logger.info(f"Starting HTML to PDF conversion with output: {self.output}")
        try:
            pdfkit.from_string(input=self.html_data, output_path=self.output)
        except Exception as error:
            logger.error(f"Error while converting HTML to PDF. \n{error}")
            return False
        return True