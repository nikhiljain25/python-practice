# AGENTS.md - AI Coding Guide

This codebase is a **Python learning project** for practicing data extraction, processing, and database operations on PDF chemistry questions. It demonstrates integration of multiple technologies through a single unified configuration system.

## Architecture Overview

### Core Components

The project follows a **modular, question-focused architecture** with three interconnected workflows:

1. **PDF Extraction Pipeline** (`q1_pdf_reader.py`, `q4_and_q6_read_regex_content.py`)
   - Reads raw PDFs and extracts text using PyPDF library
   - Applies regex patterns to parse structured Q&A content from PDF text
   - Pattern: `\d+\.\s*(.*?)\n.*?Answer:\s*([A-D]\)\s*.*)` captures question and answer pairs

2. **Data Processing & Storage** (`q5_insert_data.py`, `q5_print_saved_questions.py`)
   - Extracts Q&A pairs from search results and inserts into MySQL
   - Reads/writes to `freedb_python_mysql_db` at `sql.freedb.tech`
   - Table schema: `questions(id INT AUTO_INCREMENT PRIMARY KEY, question TEXT, answer TEXT)`

3. **Utility Operations** 
   - **Folder traversal** (`q2_traverse_folder.py`): Recursively finds PDFs, converts to text files
   - **URL content grabbing** (`q7_hit_URL_grab_text.py`): Fetches RSS feeds, parses XML links, extracts webpage content
   - **Custom page reading** (`q3_read_custom_pages.py`): Isolates specific chapters by regex patterns

### Critical Data Flow

```
PDF File → read_pdf_text() → extract_questions(regex) → search_by_regex() 
    ↓
Parse with regex pattern → (question, answer) tuple
    ↓
insert_question() → MySQL → print_all_saved_questions()
```

## Configuration System

**All paths, patterns, and credentials are externalized** in `config/config.ini` via `read_config.py`:

```python
get_config_value(section, key)  # Returns string value from config.ini
```

**Sections:**
- `[search]`: Regex patterns for content searching (`search_0` through `search_9`)
- `[regex]`: Complex patterns for parsing (e.g., `question_answer_pattern`)
- `[mysql]`: SQL queries for CRUD operations
- `[files]`: Input/output paths (hardcoded user paths, requires updating)
- `[urls]`: RSS feed URLs for external data

⚠️ **Note**: File paths in config reference `C:/Users/chigavid/codebase/` - these are hardcoded and will fail on other machines. Relative paths should be used instead.

## Project-Specific Patterns & Conventions

### Regex-Heavy Text Processing
The codebase relies heavily on regex for parsing unstructured PDF content. Key patterns:
- Question-answer pairs: `\d+\.\s*(.*?)\n.*?Answer:\s*([A-D]\)\s*.*)`
- Chapter extraction: `(Chapter\s+{chapter_no}:.*?)(?=Chapter\s+\d+:|\Z)` with `re.DOTALL | re.IGNORECASE`
- Use `re.escape()` when building dynamic patterns to avoid injection

### MySQL Integration
- Hardcoded credentials in `mysql_connection.py` (⚠️ Security issue - should use environment variables)
- Always call `conn.commit()` after `cursor.execute()` for INSERT/DELETE operations
- Pattern: Get connection → execute query → fetch results → close both cursor and connection
- Random selection: Scripts use `random.randint()` to pick search patterns dynamically

### Modular Import Pattern
Files are organized in `python_practice_programs/project/` and import from `read_config`:
```python
from project.read_config import get_config_value
from project.mysql_connection import get_mysql_conn
```

**Inconsistency Alert**: Some files use relative imports (`from project.X`), others use absolute imports. When adding new scripts, follow the `from project.module_name import` pattern to be discoverable from the main context.

### Error Handling
- File operations: Catch `FileNotFoundError`, `PermissionError`, and generic `Exception`
- Config operations: Catch `configparser.NoSectionError` and `configparser.NoOptionError` (note: one has typo in code)
- HTTP requests: Catch `requests.exceptions.RequestException`
- XML parsing: Catch `ET.ParseError`

## Key Workflows & Entry Points

| Script | Purpose | Run From | Key Dependencies |
|--------|---------|----------|------------------|
| `q1_pdf_reader.py` | Copy PDF file to output text file | Direct | `read_config` |
| `q2_traverse_folder.py` | Find all PDFs in directory, convert to text | Direct | `read_config` |
| `q4_and_q6_read_regex_content.py` | Search PDF by regex or chapter number | Interactive (stdin) | PyPDF, `read_config` |
| `q5_insert_data.py` | Random search + insert matched Q&A to MySQL | Direct | MySQL, regex matching |
| `q5_print_saved_questions.py` | Display all questions in MySQL table | Direct | MySQL |
| `q7_hit_URL_grab_text.py` | Fetch RSS feed, parse XML, grab URL content | Direct | BeautifulSoup, requests, XML parsing |
| `mysql_table_creation.py` | Initialize questions table in MySQL | Direct | MySQL |
| `delete_table_data.py` | Truncate all data from questions table | Direct | MySQL |

## Important Gotchas & Conventions

1. **Relative Path Issues**: `read_config.py` uses `os.path.join('../config', 'config.ini')` - scripts must be run from `project/` directory
2. **Hardcoded Credentials**: MySQL password and user visible in source - refactor to environment variables
3. **Row Count Logic Bug**: `delete_table_data.py` has inverted logic (`if cursor.rowcount > 0: print('No rows deleted!')`)
4. **Mixed Import Styles**: Some scripts use relative imports, others use package paths - inconsistent but functional
5. **Random Patterns**: Several scripts use `random.randint()` for non-deterministic search selection - useful for testing variety
6. **XML/BeautifulSoup Integration**: `q7_hit_URL_grab_text.py` demonstrates combining ElementTree + BeautifulSoup for parsing

## External Dependencies

```
mysql-connector-python  # MySQL database operations
pypdf                   # PDF text extraction (used as 'from pypdf import PdfReader')
requests                # HTTP requests
beautifulsoup4          # HTML/XML parsing
```

## Testing & Debugging Approach

- Scripts have `if __name__ == "__main__"` guards for direct execution and import safety
- Config-driven approach allows testing different search patterns without code changes
- Random selection in some scripts enables testing against varied input data
- MySQL operations can be isolated by modifying `config.ini` to point to test database

---

**Last Updated**: Project structure analyzed as learning/practice codebase with production patterns (config externalization, error handling) mixed with development practices (hardcoded credentials, relative paths).

