import PyPDF2

pdf_file = "file.pdf"

pdf_read = PyPDF2.PdfFileReader(pdf_file)

for i in range(pdf_read.getNumPages()):
    page = pdf_read.getPage(i)
    print('page no: ' + str(1 + pdf_read.getPageNumber(page)))
    pageContent = page.extractText()
    if i == 1:
        print(pageContent)