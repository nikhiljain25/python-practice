import sys
import os

# Add the parent directory (python_practice_programs) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from read_config import get_config_value
from pypdf import PdfReader


def read_pdf_text(filename):
    """Extract text from PDF file using PyPDF"""
    try:
        with open(filename, "rb") as file:
            pdf_reader = PdfReader(file)
            text = ""
            
            # Extract text from all pages
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- Page {page_num + 1} ---\n"
                        text += page_text
                except Exception as e:
                    print(f"Warning: Could not extract text from page {page_num + 1}: {e}")
            
            if not text.strip():
                print("Warning: No text could be extracted from the PDF. The PDF may be image-based or encrypted.")
            
            return text
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while reading the PDF: {e}")
        return None


def write_to_file(filename, output_filename):
    """Extract text from PDF and write to output file"""
    try:
        file_content = read_pdf_text(filename)
        if file_content is None:
            return
        with open(output_filename, "w", encoding="utf-8") as file:
            file.write(file_content)
            print(f"The file {output_filename} was successfully written with {len(file_content)} characters.")
    except Exception as e:
        print(f"An unexpected error occurred while writing the file: {e}")


if __name__ == "__main__":
    input_file = get_config_value('files', 'input_file')
    output_file = get_config_value('files', 'output_file')
    write_to_file(input_file, output_file)
