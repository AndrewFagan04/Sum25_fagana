# importing required classes
from pypdf import PdfReader

# creating a pdf reader object
reader = PdfReader('cs_108_class_16_mar_21.ppt')

# printing number of pages in pdf file
print(len(reader.pages))

# creating a page object
page = reader.pages[0]

# extracting text from page
print(page.extract_text())