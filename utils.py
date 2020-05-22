import os
import PyPDF2
import zipfile

ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def pdf_split(file_path, pdf_file_name):
    pdf_file_obj = open(os.path.join(file_path, pdf_file_name), 'rb')

    # creating a pdf reader object
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)

    # printing number of pages in pdf file
    # print(pdf_reader.numPages)
    output_path = os.path.join(file_path, str(pdf_file_name).rstrip(".pdf"))
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    for page_i in range(0, pdf_reader.numPages):
        # creating a page object for each page
        page_obj = pdf_reader.getPage(page_i)

        pdfWriter = PyPDF2.PdfFileWriter()
        pdfWriter.addPage(page_obj)

        new_file = open(os.path.join(output_path, str(page_i + 1) + ".pdf"), 'wb')

        # closing the new pdf file object
        pdfWriter.write(new_file)
        new_file.close()
    pdf_file_obj.close()

    # Convert into zip
    zipf = zipfile.ZipFile(os.path.join(file_path, str(pdf_file_name).replace("pdf", "zip")), 'w', zipfile.ZIP_DEFLATED)

    for pdf_file in os.listdir(output_path):
        print(pdf_file)
        zipf.write(os.path.join(output_path, pdf_file), arcname=pdf_file)

    zipf.close()
