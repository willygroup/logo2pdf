#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, filetype, requests
from PyPDF2 import PdfFileWriter, PdfFileReader

def create_watermark(input_pdf, output, watermark):
    watermark_obj = PdfFileReader(watermark)
    watermark_page = watermark_obj.getPage(0)

    pdf_reader = PdfFileReader(input_pdf)
    pdf_writer = PdfFileWriter()

    # Watermark all the pages
    for page in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page)
        page.mergePage(watermark_page)
        pdf_writer.addPage(page)

    with open(output, 'wb') as out:
        pdf_writer.write(out)

def createDirectories():
    if not os.path.exists('files'):
        os.makedirs('files')
    if not os.path.exists('files/nologo'):
        os.makedirs('files/nologo')
    if not os.path.exists('files/logo'):
        os.makedirs('files/logo')
    if not os.path.exists('files/logo.pdf'):
        print('No logo.pdf file found!')
        print('Trying to download from web...')
        url = 'https://github.com/willygroup/addpdflogo-py/blob/main/src/logo.pdf'
        r = requests.get(url)
        if(r.status_code == requests.codes.ok):
            with open('files/logo.pdf', 'wb') as f:
                f.write(r.content)
        else:
            print('Unable to download the example logo.pdf')
            sys.exit(1)
    kind = filetype.guess('files/logo.pdf')
    if kind is None or kind.extension != 'application/pdf':
        print('logo.pdf is not a valid pdf file!')
        sys.exit(1)

if __name__ == '__main__':

    # create directories 
    createDirectories()

    n_files = 0
    if len(sys.argv) == 1:
        try:
            for f in os.listdir("files/nologo"):
                if f.endswith(".pdf"):
                    print(os.path.join("files/nologo", f))
                    print(os.path.join("files/logo", f))
                    o_filename = os.path.join("files/nologo", f)
                    n_filename = os.path.join("files/logo", f)
                    
                    create_watermark(
                        input_pdf=o_filename, 
                        output=n_filename,
                        watermark='files/logo.pdf')
            
                    os.remove(o_filename)
                    n_files=n_files+1

        except:
            print("An exception occurred ")

        if n_files > 0:
            print("%d files processed" % n_files)
        else:
            print("No file processed")
    elif len(sys.argv) > 1:
        print (sys.argv)
        print (type(sys.argv))
        files = sys.argv
        files.remove(files[0])
        print (files )
        for f in files:
            if f.endswith(".pdf"):
                print(os.path.join("./", f))
                #~ print(os.path.join("files/logo", f))
                o_filename = os.path.join("./", f)
                n_filename = os.path.join("files/logo", f)

                create_watermark(
                    input_pdf=o_filename, 
                    output=n_filename,
                    watermark='files/logo.pdf')
                n_files=n_files+1
        


# cSpell:ignore nologo