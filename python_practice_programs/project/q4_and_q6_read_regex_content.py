import sys
import os
import random
import re

# Add the parent directory (python_practice_programs) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pypdf import PdfReader
from read_config import get_config_value


def read_pdf_text(pdf_path):
    """Extract all text from a PDF file"""
    try:
        reader = PdfReader(pdf_path)
        text = ""

        for page_num, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            except Exception as e:
                print(f"Warning: Could not extract text from page {page_num + 1}: {e}")

        return text
        
    except FileNotFoundError:
        print(f"Error: PDF file not found: {pdf_path}")
        return None
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None


def extract_questions(text):
    """Extract question-answer pairs from text using regex"""
    try:
        pattern = r"\d+\..*?Answer:.*?(?=\n\d+\.|\Z)"
        questions = re.findall(pattern, text, re.DOTALL)
        return questions
    except Exception as e:
        print(f"Error extracting questions: {e}")
        return []


def search_by_regex(pdf_path, regex):
    """Search PDF text for matches to a regex pattern"""
    try:
        text = read_pdf_text(pdf_path)
        
        if text is None:
            return []
        
        questions = extract_questions(text)

        if not questions:
            print("No questions found in the PDF.")
            return []

        results = []

        for q in questions:
            try:
                if re.search(regex, q, re.IGNORECASE):
                    results.append(q)
            except re.error as e:
                print(f"Error in regex pattern: {e}")
                continue

        return results
        
    except Exception as e:
        print(f"Error in search_by_regex: {e}")
        return []


def get_subtopic(pdf_path, subtopic):
    """Extract a specific chapter or subtopic from the PDF"""
    try:
        text = read_pdf_text(pdf_path)
        
        if text is None:
            return "Error: Could not read PDF file."

        chapter_match = re.search(r'\d+', subtopic)

        if chapter_match:
            chapter_no = chapter_match.group()
            pattern = rf"(Chapter\s+{chapter_no}:.*?)(?=Chapter\s+\d+:|\Z)"
        else:
            pattern = rf"(Chapter\s+\d+:\s*{re.escape(subtopic)}.*?)(?=Chapter\s+\d+:|\Z)"

        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)

        if match:
            return match.group(1)

        return "Subtopic not found."
        
    except Exception as e:
        print(f"Error in get_subtopic: {e}")
        return "Error retrieving subtopic."


def main():
    """Main function to handle user input and search operations"""
    try:
        input_file = get_config_value('files', 'input_file')
        
        if input_file is None:
            print("Error: Could not read input_file from configuration.")
            return
        
        regex_patterns = ['search_0', 'search_1', 'search_2']

        choice = input("Enter 1 for regex search or 2 for subtopic search: ").strip()
        
        if choice == "1":
            print("\n" + "="*60)
            print("REGEX SEARCH MODE")
            print("="*60)
            
            for regex_key in regex_patterns:
                regex_pattern = get_config_value('search', regex_key)
                if regex_pattern is None:
                    print(f"Error: Could not retrieve {regex_key} from configuration.")
                    continue

                matches = search_by_regex(input_file, regex_pattern)

                if matches:
                    print(f"\n✓ Matches found for '{regex_pattern}':")
                    print("-" * 60)
                    for match in matches:
                        print(match)
                        print("-" * 60)
                else:
                    print(f"\nℹ No matches found for '{regex_pattern}'.")

        elif choice == "2":
            print("\n" + "="*60)
            print("SUBTOPIC/CHAPTER SEARCH MODE")
            print("="*60)
            
            chapter_no = str(random.randint(1, 5))

            print(f"\nRandomly searching for Chapter {chapter_no}...")
            result = get_subtopic(input_file, "Chapter " + chapter_no)
            print("\n" + "-"*60)
            print(result)
            print("-"*60)
        else:
            print("Invalid choice. Please enter 1 or 2.")
            
    except KeyboardInterrupt:
        print("\n\nSearch cancelled by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
