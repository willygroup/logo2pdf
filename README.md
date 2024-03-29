# addpdflogo-py
Add logo to PDF files

## Installation
 - Create the python virtual environment with the command:
   ```bash
   $ source create_python_venv_linux.sh
   ```
 - Launch the script as:
   ```bash
   $ python main.py <file_list>
   ```

## Usage
 - File list from directory:
   - Place the files you need to add the logo to in the *files/nologo* directory
   - Copy a pdf file with your logo in *files/logo.pdf* (overwrite the existing file if necessary)
   - Run the program
   - Check the *files/logo* directory for the new pdf files with you logo
   - _Warning:_ This will erase the input files!!!
 - File list from command-line
   - Call the script adding the file list as arguments:
     ```bash
     $ python main.py <file_1.pdf> <file_2.pdf> ... <file_n.pdf>
     ```
   - Check the *files/logo* directory for the new pdf files with you logo

### Packages required (see `requirements.txt`)
 - PyPDF2
 - filetype
 - os, sys, requests


 ## Start the application with a different language in linux
 ```bash
 $ LANG=it_IT.UTF-8 python main.py
 $ LANG=en_US.UTF-8 python main.py 
 ```

## Create .po translation file
 ```bash 
 $ xgettext main.py 
 ```
 This will create a `message.po` file in the root directory.

## Create .mo translation file from .po
 ```bash
 $ msgfmt files/locale/it_IT/LC_MESSAGES/csv2lbl.po -o files/locale/it_IT/LC_MESSAGES/csv2lbl.mo
 ```