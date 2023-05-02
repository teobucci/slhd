import os
import nbformat
from tqdm import tqdm
from nbconvert import PDFExporter

# Get the current directory path
folder_path = os.getcwd()

# Get all ipynb files in current directory
files = [f for f in os.listdir() if f.endswith('.ipynb')]

# Set up the PDF exporter
pdf_exporter = PDFExporter()

# Iterate over the ipynb files and convert to PDF
for file in tqdm(files):
    with open(file) as f:
        nb_contents = nbformat.read(f, as_version=nbformat.NO_CONVERT)
        
        # Use the PDFExporter to convert the notebook object to a PDF file
        pdf_data, _ = pdf_exporter.from_notebook_node(nb_contents)
        
        # Create a file name for the PDF file
        pdf_file_name = file.replace(".ipynb", ".pdf")
        
        # Create a path for the PDF file
        pdf_file_path = os.path.join(folder_path, pdf_file_name)
        
        # Write the PDF data to a file
        with open(pdf_file_path, "wb") as pdf_file:
            pdf_file.write(pdf_data)
