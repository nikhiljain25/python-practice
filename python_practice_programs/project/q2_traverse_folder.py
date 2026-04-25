import sys
import os
import fnmatch

# Add the parent directory (python_practice_programs) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from read_config import get_config_value
from pypdf import PdfReader


def extract_pdf_text(input_filename):
    """Extract text from a PDF file"""
    try:
        with open(input_filename, "rb") as file:
            pdf_reader = PdfReader(file)
            text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- Page {page_num + 1} ---\n"
                        text += page_text
                except Exception as e:
                    print(f"Warning: Could not extract text from page {page_num + 1} of {input_filename}: {e}")
            return text
    except FileNotFoundError:
        print(f"Error: The file {input_filename} was not found.")
        return None
    except PermissionError:
        print(f"Error: Permission denied for file {input_filename}.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while reading {input_filename}: {e}")
        return None


def process_pdf(input_filename, output_filename):
    """Extract text from PDF and write to output file"""
    try:
        text_content = extract_pdf_text(input_filename)
        
        if text_content is None:
            return False
        
        with open(output_filename, "w", encoding="utf-8") as file:
            file.write(text_content)
        
        print(f"✓ Successfully processed: {input_filename} → {output_filename}")
        return True
        
    except PermissionError:
        print(f"Error: Permission denied while writing to {output_filename}.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while processing {input_filename}: {e}")
        return False


def find_pdf(directory):
    """Recursively find all PDF files in a directory"""
    pdf_files_list = []
    try:
        for root, dirs, files in os.walk(directory):
            for found_filename in fnmatch.filter(files, '*.pdf'):
                pdf_files_list.append(os.path.join(root, found_filename))
    except PermissionError:
        print(f"Error: Permission denied accessing directory {directory}.")
    except Exception as e:
        print(f"An unexpected error occurred while traversing directory: {e}")
    
    return pdf_files_list


if __name__ == '__main__':
    try:
        file_path = get_config_value('files', 'file_path')
        
        if file_path is None:
            print("Error: Could not read file_path from configuration.")
            sys.exit(1)
        
        if not os.path.exists(file_path):
            print(f"Error: Directory {file_path} does not exist.")
            sys.exit(1)
        
        print(f"Searching for PDF files in: {file_path}\n")
        pdf_files = find_pdf(file_path)
        
        if not pdf_files:
            print("No PDF files found in the directory.")
            sys.exit(0)
        
        print(f"Found {len(pdf_files)} PDF file(s):\n")
        
        processed_count = 0
        for filename in pdf_files:
            print(f"Processing: {filename}")
            base_name = os.path.splitext(filename)[0]
            op_filename = f"{base_name}_output.txt"
            
            if process_pdf(filename, op_filename):
                processed_count += 1
        
        print(f"\n✓ Successfully processed {processed_count}/{len(pdf_files)} PDF files.")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
