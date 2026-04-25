import os
import sys

# Add the parent directory (python_practice_programs) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pypdf import PdfReader
from read_config import get_config_value


def write_pdf(input_file, output_file, pages):
    """Extract specific pages from PDF and write to output file"""
    try:
        if not os.path.exists(input_file):
            print(f"Error: The input file {input_file} does not exist.")
            return False

        reader = PdfReader(input_file)
        
        try:
            with open(output_file, "w", encoding="utf-8") as file:
                for page in pages:
                    try:
                        page_number = int(page)
                        
                        if page_number < 0 or page_number >= len(reader.pages):
                            print(f"Error: Page number {page_number} is out of range (PDF has {len(reader.pages)} pages)")
                            continue
                        
                        page_content = reader.pages[page_number].extract_text()
                        file.write(f"\n{'='*60}\n")
                        file.write(f"Page {page_number + 1}\n")
                        file.write(f"{'='*60}\n")
                        file.write(page_content)
                        file.write("\n\n")
                        
                        print(f"\n{'='*60}")
                        print(f"✓ Page {page_number + 1} extracted successfully")
                        print(f"{'='*60}")
                        print(page_content[:200] + "..." if len(page_content) > 200 else page_content)
                        
                    except ValueError:
                        print(f"Error: '{page}' is not a valid page number. Please enter integers.")
                    except IndexError:
                        print(f"Error: Page number {page_number} does not exist.")
                    except Exception as e:
                        print(f"Error extracting page {page}: {e}")
            
            print(f"\n✓ Successfully wrote extracted pages to {output_file}")
            return True
            
        except FileNotFoundError:
            print(f"Error: The output directory does not exist for {output_file}.")
            return False
        except PermissionError:
            print(f"Error: Permission denied while writing to {output_file}.")
            return False
        except Exception as e:
            print(f"An unexpected error occurred while writing the file: {e}")
            return False
            
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def main():
    """Main function to handle command-line arguments"""
    try:
        if len(sys.argv) < 2:
            print("Usage: python q3_read_custom_pages.py <page_number> [<page_number> ...]")
            print("Example: python q3_read_custom_pages.py 0 1 2")
            sys.exit(1)

        input_file = get_config_value('files', 'input_file')
        
        if input_file is None:
            print("Error: Could not read input_file from configuration.")
            sys.exit(1)
        
        output_file = get_config_value('files', 'output_file')
        
        if output_file is None:
            print("Error: Could not read output_file from configuration.")
            sys.exit(1)

        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            print(f"Error: The output directory {output_dir} does not exist.")
            sys.exit(1)

        pages = sys.argv[1:]
        write_pdf(input_file, output_file, pages)
        
    except Exception as e:
        print(f"An unexpected error occurred in main: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
