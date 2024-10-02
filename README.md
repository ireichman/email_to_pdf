# email_to_pdf

## A simple way to convert multiple eml files to PDFs with a naming scheme.

## THIS IS A VERY EARLY VERSION. Use at your own risk.
### Roadmap:
* Add ability to save multiple emails to one PDF.
* Add ability to process a CSV with a list of emails and corresponding PDF names.
* Add ability to process eml file directly from an archive.
* Add ability to zip PDF files.
* Create executables.
* Add GUI.
* Add WUI.
* Add ability to forward emails to the software and receive an email back with PDF attachment.


### Arguments:
`-s` / `--source` - Specify which file(s) to convert.  
`-o` / `--output` - Specify path to save converted files in.  
`on` / `--output_name` - Specify the name and, optionally, path of output file(s). If more than one file is converted, 
  files will be generated as "file.pdf", "file-1.pdf", etc.  


### Instructions:
* This application requires python 3.12 installed on your system.
* In addition wkhtmltopdf is required. It can be installed on Ubuntu / Debian with `sudo apt install wkhtmltopdf`, 
  or find a download for your platofrm [here](https://wkhtmltopdf.org/downloads.html).
* Run tha application using `python main.py --source <file1.eml file2.eml>` This will convert the emails while keeping
  their file names. 
* If you would like files ot be saved with a specific name and path, use `-on`. `python main.py -source <file1.eml, file2.eml>
  -on </path/to/folder/file_name.pdf>`. This convention will save files using the output name given and add serial numbers athe end.
* If you would like to keep the original file name but save to a different directory than the one you run the program from, 
  use `--output`. `python main.py --source <file1.eml file2.eml> --output </some/folder/>`
