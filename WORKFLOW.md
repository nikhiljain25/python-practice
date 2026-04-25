# Practice Program - Project Workflow Definition

## 🎯 Project Purpose
A Python learning project designed to **extract chemistry exam questions from PDF documents**, **process them using regex patterns**, **store them in a MySQL database**, and **retrieve content from external web sources**.

---

## 📊 Complete Workflow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRACTICE PROGRAM ECOSYSTEM                    │
└─────────────────────────────────────────────────────────────────┘

                         CONFIG LAYER (config.ini)
                    ↓       ↓       ↓       ↓       ↓
        ┌──────────────────┬──────────────┬────────────────┐
        │                  │              │                │
    PDF INPUT        TEXT OUTPUT      MYSQL DB      EXTERNAL URLs
   (Chemistry          (Extracted     (Questions)    (RSS Feeds)
    Questions)         Content)
```

---

## 🔄 Four Main Operational Workflows

### **WORKFLOW 1: PDF → TEXT Conversion Pipeline**

#### Entry Points:
- `q1_pdf_reader.py` - Single file conversion
- `q2_traverse_folder.py` - Batch PDF conversion

#### Process:
```
Read PDF File (binary)
    ↓
Extract raw bytes
    ↓
Write to TEXT file
    ↓
Output: .txt files in same directory with "_output" suffix
```

#### Example Execution:
```bash
python q1_pdf_reader.py
# Reads: C:/Users/chigavid/codebase/content/Chemistry Questions.pdf
# Writes: C:/Users/chigavid/codebase/content/output.txt

python q2_traverse_folder.py
# Finds ALL PDFs recursively in directory
# Converts: Chemistry Questions.pdf → Chemistry Questions_output.txt
#           Chemistry Questions_1.pdf → Chemistry Questions_1_output.txt
#           Chemistry Questions_3.pdf → Chemistry Questions_3_output.txt
```

**Config Dependencies:**
- `config.ini [files]`: `input_file`, `output_file`, `file_path`

---

### **WORKFLOW 2: PDF → Regex Search → Q&A Extraction**

#### Entry Point:
- `q4_and_q6_read_regex_content.py` - Interactive search utility

#### Two Sub-Workflows:

**A) Regex Pattern Search**
```
User Input: "1" (choose regex search)
    ↓
Load Search Patterns (search_0 through search_2)
    ↓
For each pattern:
  1. Read PDF file
  2. Extract all text
  3. Apply regex pattern to find matches
  4. Display matching questions
    ↓
Output: Console display of matched Q&A pairs
```

**B) Chapter/Subtopic Extraction**
```
User Input: "2" (choose chapter search)
    ↓
Randomly select chapter (1-5)
    ↓
Build dynamic regex: (Chapter\s+{chapter_no}:.*?)(?=Chapter\s+\d+:|\Z)
    ↓
Extract chapter content with DOTALL + IGNORECASE flags
    ↓
Output: Full chapter text to console
```

**Key Functions:**
- `read_pdf_text(pdf_path)` → Extract all text from PDF
- `extract_questions(text)` → Parse questions using pattern: `\d+\..*?Answer:.*?(?=\n\d+\.|\Z)`
- `search_by_regex(pdf_path, regex)` → Filter questions matching regex
- `get_subtopic(pdf_path, subtopic)` → Extract specific chapter

**Config Dependencies:**
- `config.ini [search]`: patterns `search_0` through `search_2`
- `config.ini [files]`: `input_file`

---

### **WORKFLOW 3: PDF → MySQL Database Storage**

#### Entry Point:
- `q5_insert_data.py` - Automated search and insert

#### Process:
```
1. RANDOM SELECTION
   ├─ Pick random search pattern (search_0 to search_9)
   └─ Example: "2. What happens to the"

2. SEARCH & EXTRACT
   ├─ Search PDF for matching content
   ├─ Apply regex pattern to extract Q&A pair
   │  Pattern: \d+\.\s*(.*?)\n.*?Answer:\s*([A-D]\)\s*.*)
   └─ Capture groups: (question, answer)

3. DATABASE INSERT
   ├─ Get MySQL connection
   ├─ Execute: INSERT INTO questions (question, answer) VALUES (?, ?)
   ├─ Commit transaction
   └─ Verify: cursor.rowcount > 0

4. DISPLAY RESULTS
   └─ Call print_all_saved_questions() to show updated table
```

**Database Details:**
- **Host:** sql.freedb.tech
- **Database:** freedb_python_mysql_db
- **Credentials:** freedb_gavidi / #u2Fr!eRkwt*F6n (⚠️ Exposed in code)
- **Table Schema:**
  ```sql
  CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT,
    answer TEXT
  )
  ```

**Key Functions:**
- `search_by_regex(pdf_path, regex)` → Find matching questions
- `insert_question(question, answer)` → Store in MySQL
- `print_all_saved_questions()` → Display all rows

**Config Dependencies:**
- `config.ini [search]`: All 10 patterns for random selection
- `config.ini [mysql]`: `insert_query_1`
- `config.ini [files]`: `input_file`

---

### **WORKFLOW 4: Web Scraping Pipeline**

#### Entry Point:
- `q7_hit_URL_grab_text.py` - Fetch external content

#### Process:
```
1. FETCH RSS FEED
   ├─ Retrieve URL: https://www.w3schools.com/xml/xml_rss.asp
   └─ Extract HTML content

2. PARSE XML FROM HTML
   ├─ Find div with class="w3-code notranslate htmlHigh"
   ├─ Extract raw XML text
   └─ Parse with ElementTree

3. EXTRACT LINK URLS
   ├─ Find all <link> elements in XML
   ├─ Remove duplicates (use set)
   └─ Example URLs from RSS

4. FETCH EACH URL
   ├─ For each unique URL:
   │  ├─ GET request
   │  ├─ Extract HTML content
   │  └─ Append to buffer
   └─ Separator: ======================================

5. WRITE OUTPUT
   └─ Save all content to: C:/Users/chigavid/codebase/content/output_url_content.txt
```

**Key Functions:**
- `fetch_url_content(url)` → HTTP GET with error handling
- `fetch_urls_list()` → Orchestrate entire pipeline
- `write_to_file(content)` → Persist combined results

**Error Handling:**
- `requests.exceptions.RequestException` → Network/HTTP errors
- `ET.ParseError` → Malformed XML

**Config Dependencies:**
- `config.ini [urls]`: `rss_url`

---

## 📋 Supporting Operations

### **Database Initialization & Maintenance**

#### `mysql_table_creation.py`
```
Purpose: Initialize database schema
├─ Get MySQL connection
├─ Execute: CREATE TABLE IF NOT EXISTS questions (...)
├─ Commit
└─ Close connection
```

#### `q5_print_saved_questions.py`
```
Purpose: View all stored questions
├─ Query: SELECT * FROM questions
├─ Display each row: (id, question, answer)
└─ Used by q5_insert_data.py as callback
```

#### `delete_table_data.py`
```
Purpose: Clear all data
├─ Execute: TRUNCATE TABLE questions
├─ ⚠️ BUG: Inverted logic in output message
│  if cursor.rowcount > 0:
│      print('No rows deleted!')  # WRONG - should print deleted
└─ Fix needed: Invert condition
```

---

## 🔌 Configuration System (Single Source of Truth)

All scripts reference **`config/config.ini`** via `read_config.py`:

```python
def get_config_value(section, key):
    """Load configuration value from config.ini"""
    config_file = os.path.join('../config', 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_file)
    return config.get(section, key)
```

### Config Structure:
```ini
[search]           # 10 regex patterns (search_0 to search_9)
[regex]            # Q&A extraction pattern
[mysql]            # CRUD SQL queries
[files]            # Hardcoded file paths ⚠️
[urls]             # RSS feed URLs
```

### ⚠️ Critical Configuration Issues:
1. **Hardcoded Paths:** All paths reference `C:/Users/chigavid/codebase/`
2. **Relative Path Bug:** `read_config.py` uses `../config/config.ini` - requires running from `project/` directory
3. **Exposed Credentials:** MySQL user/password in config and source code

---

## 🔄 Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                        INPUT SOURCES                             │
│  ┌─────────────┐          ┌──────────────┐     ┌──────────────┐ │
│  │ PDF Files   │          │ config.ini   │     │ External URLs│ │
│  │ (Chemistry  │          │ (Patterns &  │     │ (RSS Feeds)  │ │
│  │ Questions)  │          │  Paths)      │     │              │ │
│  └──────┬──────┘          └──────┬───────┘     └──────┬───────┘ │
└─────────┼──────────────────────────┼────────────────────┼─────────┘
          │                          │                    │
          ▼                          ▼                    ▼
      ┌──────────────────────────────────────────────────────┐
      │           PROCESSING LAYER (Python Scripts)          │
      │  ┌─────────────┐ ┌──────────┐ ┌────────┐ ┌────────┐ │
      │  │ q1_q2: PDF  │ │q4_q6:   │ │q5:    │ │q7:     │ │
      │  │ ↔ TEXT      │ │Regex    │ │Insert │ │Web     │ │
      │  │ Convert     │ │Search   │ │Data   │ │Scrape  │ │
      │  └─────────────┘ └──────────┘ └────────┘ └────────┘ │
      │         │               │           │           │    │
      └─────────┼───────────────┼───────────┼───────────┼────┘
                │               │           │           │
                ▼               ▼           ▼           ▼
      ┌──────────────────────────────────────────────────────┐
      │           OUTPUT DESTINATIONS                        │
      │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐  │
      │  │Text      │ │Console   │ │MySQL     │ │Output  │  │
      │  │Files     │ │Display   │ │Database  │ │Files   │  │
      │  │(*.txt)   │ │(stdout)  │ │questions │ │(web)   │  │
      │  └──────────┘ └──────────┘ └──────────┘ └────────┘  │
      └──────────────────────────────────────────────────────┘
```

---

## 🚀 Execution Flow Examples

### **Example 1: Extract & Insert a Random Question**
```bash
cd python_practice_programs/project
python q5_insert_data.py

# Step by step:
# 1. Randomly pick search_7 = "3."
# 2. Search PDF for questions starting with "3."
# 3. Parse with regex: \d+\.\s*(.*?)\n.*?Answer:\s*([A-D]\)\s*.*)
# 4. Extract first match: (question, answer)
# 5. INSERT into MySQL: INSERT INTO questions VALUES (?, ?)
# 6. Commit transaction
# 7. Display all questions in table
```

### **Example 2: Interactive Regex Search**
```bash
cd python_practice_programs/project
python q4_and_q6_read_regex_content.py

Enter 1 for regex search or 2 for subtopic search: 1
# Searches for search_0, search_1, search_2 patterns
# Displays: "Matches found for = 2. What happens to the"

# Or choose option 2:
Enter 1 for regex search or 2 for subtopic search: 2
# Randomly picks Chapter (1-5)
# Extracts and displays full chapter
```

### **Example 3: Batch Convert All PDFs**
```bash
cd python_practice_programs/project
python q2_traverse_folder.py

# Recursively finds:
# - /content/Chemistry Questions.pdf → Chemistry Questions_output.txt
# - /content/one/Chemistry Questions_1.pdf → Questions_1_output.txt
# - /content/two/Chemistry Questions_2.pdf → Questions_2_output.txt
# - /content/three/Chemistry Questions_3.pdf → Questions_3_output.txt
```

---

## 🛠️ Technical Stack

| Component | Technology | Notes |
|-----------|-----------|-------|
| **PDF Processing** | PyPDF | `from pypdf import PdfReader` |
| **Text Processing** | Regex (re) | DOTALL, IGNORECASE flags used |
| **Database** | MySQL 5.7+ | Via mysql-connector-python |
| **Web Scraping** | Requests + BeautifulSoup4 | HTML parsing & HTTP |
| **XML Parsing** | ElementTree | For RSS feed parsing |
| **Configuration** | ConfigParser | External config.ini file |

---

## 🐛 Known Issues & Gotchas

1. **Path Resolution Bug**
   - `read_config.py` assumes running from `project/` directory
   - Relative path: `../config/config.ini` fails if run from parent directory

2. **Hardcoded Paths in config.ini**
   - All paths reference `C:/Users/chigavid/codebase/`
   - Will fail on any other machine
   - Needs migration to environment variables or relative paths

3. **Security Vulnerabilities**
   - MySQL credentials exposed in source code
   - Hardcoded password in `mysql_connection.py`
   - No encryption or environment variable usage

4. **Logic Bug in delete_table_data.py**
   ```python
   if cursor.rowcount > 0:
       print('No rows deleted!')  # ← INVERTED
   else:
       print('All rows deleted!')
   ```

5. **Import Inconsistency**
   - Some files use: `from project.module import`
   - Others use: `from module import`
   - Causes import errors when run from different directories

6. **Non-deterministic Testing**
   - `q5_insert_data.py` uses `random.randint()` for pattern selection
   - Makes debugging and testing unpredictable
   - Should accept pattern as parameter instead

---

## 📈 Data Volume & Performance Considerations

- **PDF Size:** Typical chemistry PDFs with multiple questions
- **Regex Performance:** Linear scan through entire PDF text
- **Database:** Small-scale free tier MySQL (freedb.tech)
- **Scalability:** Not suitable for large document volumes without optimization

---

## 🔗 Module Dependency Graph

```
┌─────────────────────────────────────────────┐
│           read_config.py (Core)             │
│     Provides: get_config_value()            │
└────────────┬────────────────────────────────┘
             │
    ┌────────┴────────┬────────────────┐
    │                 │                │
    ▼                 ▼                ▼
q1/q2/q3/q4     q5_insert_data.py    q7
pdf_reader       (imports q4, q5)    url_scraper
    │            mysql_connection    
    │                 │              
    └─────────────────┴──────────────►MySQL DB
```

---

## ✅ Summary: Complete Workflow

```
1. USER CHOOSES OPERATION
   ├─ Extract text from PDF
   ├─ Search questions by regex
   ├─ Insert questions into database
   ├─ View all questions
   └─ Fetch external web content

2. LOAD CONFIGURATION
   └─ Read config.ini for paths, patterns, credentials

3. PROCESS DATA
   ├─ Read PDF/URLs
   ├─ Parse using regex or XML
   ├─ Transform to structured format
   └─ Filter/search as needed

4. STORE/OUTPUT
   ├─ Write to MySQL database
   ├─ Write to text files
   └─ Display to console

5. FEEDBACK LOOP
   └─ Display results for verification
```

This workflow demonstrates a complete data pipeline from unstructured PDF documents through structured storage and external data integration.

