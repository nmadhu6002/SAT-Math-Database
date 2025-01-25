import os
import fitz  # PyMuPDF
from tqdm import tqdm  # For progress bars

# Define the base directory containing the PDFs and the new base directory for the output
base_directory = "PDF_Database"
output_base_directory = "Image_Database"  # Change this to the desired output directory

total_pdfs = 0
total_pages = 0

# Walk through all directories and files in the base directory
for root, _, files in tqdm(os.walk(base_directory), desc="Folders processed"):
    pdf_files = [file for file in files if file.endswith(".pdf")]  # Filter PDF files

    for file in tqdm(pdf_files, desc=f"Processing PDFs in {root}", leave=False):
        total_pdfs += 1
        pdf_path = os.path.join(root, file)  # Full path to the PDF

        # Recreate the folder structure in the output base directory
        relative_path = os.path.relpath(root, base_directory)  # Path relative to the base directory
        output_folder = os.path.join(output_base_directory, relative_path, file[:-4])  # Replace .pdf with folder

        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Open the PDF
        doc = fitz.open(pdf_path)

        # Convert each page to a PNG and save
        for page in tqdm(doc, desc=f"Converting pages of {file}", leave=False):
            total_pages += 1
            pixmap = page.get_pixmap(dpi=300)
            output_path = os.path.join(output_folder, f"problem-{page.number + 1}.png")
            pixmap.save(output_path)

# Summary of the process
print("\nConversion complete!")
print(f"Total PDFs processed: {total_pdfs}") # 114
print(f"Total pages converted to PNG: {total_pages}") # 1712