# Python/Go/Java Project - Chemistry Question Extraction & Storage

A comprehensive Python learning project demonstrating PDF processing, regex patterns, MySQL integration, and web scraping with proper error handling and configuration management.

## 🎯 Project Overview

This project implements **8 progressive projects** (Projects 1-8) that build upon each other to create a complete data extraction and storage pipeline.

### **Project Summary:**

| Project | Name | Status |
|---------|------|--------|
| 1 | Read PDF & Write to Text | ✅ Complete |
| 2 | Traverse Folders & Batch Process PDFs | ✅ Complete |
| 3 | Read Specific Pages from PDF | ✅ Complete |
| 4 | Regex Pattern Extraction from Config | ✅ Complete |
| 5 | Store Extracted Questions in MySQL | ✅ Complete (+ Bulk Insert) |
| 6 | Load Questions by Chapter | ✅ Complete |
| 7 | RSS Content Extraction & Web Scraping | ✅ Complete |
| 8 | OOPs/Inheritance for Question Types | ⏳ Future |

---

## 📁 Project Structure

```
practice program/
├── README.md                          # This file
├── AGENTS.md                          # AI agent programming guide
├── WORKFLOW.md                        # Complete workflow documentation
├── PROJECT6_IMPLEMENTATION_GUIDE.md  # Project 6 setup guide
├── BULK_INSERT_GUIDE.md              # Bulk insert instructions
├── BULK_INSERT_VERIFICATION.md       # Verification guide
├── .gitignore                        # Git ignore rules
├── .git/                             # Git repository
│
├── python_practice_programs/
│   ├── main.py                       # Main entry point
│   ├── config/
│   │   └── config.ini               # Configuration file
│   │
│   ├── project/                     # Main project directory
│   │   ├── q1_pdf_reader.py         # Project 1: Read single PDF
│   │   ├── q2_traverse_folder.py    # Project 2: Batch process PDFs
│   │   ├── q3_read_custom_pages.py  # Project 3: Read custom pages
│   │   ├── q4_and_q6_read_regex_content.py  # Project 4: Regex extraction
│   │   ├── q5_insert_data.py        # Project 5: Insert random question
│   │   ├── q5_bulk_insert_all_questions.py  # Project 5: Bulk insert ALL
│   │   ├── q5_print_saved_questions.py      # Project 5: Display questions
│   │   ├── q6_load_chapter_questions.py     # Project 6: Search by chapter
│   │   ├── q7_hit_URL_grab_text.py  # Project 7: Web scraping
│   │   ├── mysql_connection.py      # MySQL helper functions
│   │   ├── mysql_table_creation.py  # Create database schema
│   │   ├── delete_table_data.py     # Clear database
│   │   ├── read_config.py           # Configuration reader
│   │   └── __pycache__/             # Python cache
│   │
│   └── resources/
│       ├── Chemistry Questions.pdf  # Test PDF file
│       └── ...
│
└── content/                          # Content storage
    ├── Chemistry Questions.pdf       # Input PDF
    ├── Chemistry Questions_output.txt # Output text
    ├── output_url_content.txt        # Web scraping output
    ├── one/                          # Folder 1 for Project 2
    │   ├── Chemistry Questions_1.pdf
    │   └── Chemistry Questions_1_output.txt
    ├── two/                          # Folder 2 for Project 2
    │   ├── Chemistry Questions_2.pdf
    │   └── Chemistry Questions_2_output.txt
    └── three/                        # Folder 3 for Project 2
        ├── Chemistry Questions_3.pdf
        └── Chemistry Questions_3_output.txt
```

---

## 🚀 Quick Start

### **Prerequisites**

- Python 3.8+
- MySQL (via Docker recommended)
- Docker (optional, for local MySQL)
- SQLElectron (optional, for database GUI)

### **Installation**

1. **Clone/Download project**
```bash
cd "D:\Study_Material\GenAI\practice program"
```

2. **Install dependencies**
```bash
pip install mysql-connector-python pypdf requests beautifulsoup4
```

3. **Setup database**

Option A: Use Docker (Local MySQL)
```bash
docker run -d --name python_db -e MYSQL_ROOT_PASSWORD=#u2Fr!eRkwt*F6n -e MYSQL_DATABASE=freedb_python_mysql_db -p 3306:3306 mysql:latest
```

Option B: Use Remote MySQL
```
Host: sql.freedb.tech
User: freedb_gavidi
Password: #u2Fr!eRkwt*F6n
Database: freedb_python_mysql_db
```

4. **Update config.ini** (if using different credentials)
```ini
[mysql]
host = localhost      # or sql.freedb.tech
user = root          # or freedb_gavidi
password = #u2Fr!eRkwt*F6n
database = freedb_python_mysql_db
port = 3306
```

---

## 📖 How to Run Each Project

### **Project 1: Read PDF and Write Text**
```bash
python python_practice_programs/project/q1_pdf_reader.py
```
Output: `content/output.txt`

### **Project 2: Traverse Folders & Batch Process**
```bash
python python_practice_programs/project/q2_traverse_folder.py
```
Output: Multiple `*_output.txt` files in subfolders

### **Project 3: Read Specific Pages**
```bash
python python_practice_programs/project/q3_read_custom_pages.py 0 1 2
```
Arguments: Page numbers (0-indexed)

### **Project 4: Regex Pattern Extraction**
```bash
python python_practice_programs/project/q4_and_q6_read_regex_content.py
```
Interactive menu to search by regex or chapter

### **Project 5: Insert Questions into MySQL**

**Single Insert (Random):**
```bash
python python_practice_programs/project/q5_insert_data.py
```

**Bulk Insert ALL (Recommended):**
```bash
python python_practice_programs/project/q5_bulk_insert_all_questions.py
```
When prompted: Type `yes` to confirm

**View Stored Questions:**
```bash
python python_practice_programs/project/q5_print_saved_questions.py
```

### **Project 6: Load Questions by Chapter**
```bash
python python_practice_programs/project/q6_load_chapter_questions.py "Chapter 1"
python python_practice_programs/project/q6_load_chapter_questions.py "atoms"
python python_practice_programs/project/q6_load_chapter_questions.py "1"
```

### **Project 7: Web Scraping & RSS**
```bash
python python_practice_programs/project/q7_hit_URL_grab_text.py
```
Output: `content/output_url_content.txt`

### **Database Operations**

Create tables:
```bash
python python_practice_programs/project/mysql_table_creation.py
```

Clear all data:
```bash
python python_practice_programs/project/delete_table_data.py
```

---

## 🔧 Configuration

### **config.ini Structure**

```ini
[search]
search_0 through search_9 = Regex patterns for searching

[regex]
question_answer_pattern = Pattern to extract Q&A pairs

[mysql]
host = Database host
user = Database user
password = Database password
database = Database name
port = Database port

[files]
input_file = Path to PDF file
output_file = Path to output text file
file_path = Path to folder containing PDFs

[urls]
rss_url = RSS feed URL for web scraping
```

---

## 📊 Technology Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.8+ |
| PDF Processing | PyPDF |
| Text Processing | Regex (re) |
| Database | MySQL 5.7+ |
| Web Scraping | Requests + BeautifulSoup4 |
| XML Parsing | ElementTree |
| Configuration | ConfigParser |
| Containerization | Docker (optional) |

---

## 📚 Key Features

✅ **Modular Architecture** - Separate scripts for each concern
✅ **Configuration-Driven** - All settings in config.ini
✅ **Error Handling** - Comprehensive try-except blocks
✅ **Database Integration** - Full MySQL CRUD operations
✅ **Batch Processing** - Support for multiple files
✅ **Regex Patterns** - Flexible content extraction
✅ **Web Scraping** - RSS feed parsing and URL content extraction
✅ **Command-Line Interface** - Arguments for user input
✅ **Progress Tracking** - Real-time feedback during long operations
✅ **Formatted Output** - Tables and structured displays

---

## 🐛 Error Handling

The project handles:

- ❌ **File Operations:**  `FileNotFoundError`, `PermissionError`
- ❌ **Configuration:** `NoSectionError`, `NoOptionError`
- ❌ **Database:** `mysql.connector.Error`, connection failures
- ❌ **Network:** `RequestException` for HTTP/URL issues
- ❌ **XML Parsing:** `ParseError` for malformed XML
- ❌ **User Input:** Empty strings, invalid formats

---

## 🔐 Security Notes

⚠️ **Current Implementation:**
- Credentials stored in config.ini
- Password visible in environment variables
- Suitable for learning/development only

✅ **Production Recommendations:**
- Use environment variables for credentials
- Implement secret management (AWS Secrets, HashiCorp Vault)
- Use connection pooling
- Encrypt sensitive data
- Never commit credentials to Git

---

## 📝 Git Setup

Initialize repository:
```bash
git init
git config user.name "Your Name"
git config user.email "your@email.com"
```

Add files:
```bash
git add .
git commit -m "Initial commit: Projects 1-7 complete"
```

Check status:
```bash
git status
```

---

## 📖 Documentation Files

- **AGENTS.md** - AI agent programming guide
- **WORKFLOW.md** - Complete architecture and workflows
- **PROJECT6_IMPLEMENTATION_GUIDE.md** - Detailed Project 6 setup
- **BULK_INSERT_GUIDE.md** - How to insert all questions at once
- **BULK_INSERT_VERIFICATION.md** - Verification checklist
- **PROJECT6_VERIFICATION.md** - Project 6 gap analysis

---

## 🎯 Example Workflows

### **Complete Setup Workflow (5 minutes):**

```bash
# 1. Create tables
python python_practice_programs/project/mysql_table_creation.py

# 2. Insert all questions
python python_practice_programs/project/q5_bulk_insert_all_questions.py
# Type: yes

# 3. View all questions
python python_practice_programs/project/q5_print_saved_questions.py

# 4. Search by chapter
python python_practice_programs/project/q6_load_chapter_questions.py "Chapter 1"
```

### **Development Workflow:**

```bash
# Make changes to Python files
# Edit config.ini as needed

# Test changes
python python_practice_programs/project/<script_name>.py

# Commit to Git
git add .
git commit -m "Feature: Add new capability"
```

---

## 🚀 Getting Started

1. **Start with Project 1:**
   ```bash
   python python_practice_programs/project/q1_pdf_reader.py
   ```

2. **Progress through Projects 2-4:**
   Follow the "How to Run" section above

3. **Setup MySQL & Insert Data:**
   ```bash
   python python_practice_programs/project/mysql_table_creation.py
   python python_practice_programs/project/q5_bulk_insert_all_questions.py
   ```

4. **Use Projects 5-6:**
   ```bash
   python python_practice_programs/project/q5_print_saved_questions.py
   python python_practice_programs/project/q6_load_chapter_questions.py "1"
   ```

---

## 📞 Support

Each script includes:
- Help message when run with no arguments
- Error messages with specific guidance
- Usage examples in code comments
- Configuration validation

Check individual files for detailed docstrings.

---

## 🎓 Learning Outcomes

After completing this project, you'll understand:

✅ PDF text extraction with PyPDF
✅ Regular expression pattern matching
✅ File system navigation and batch processing
✅ MySQL database operations (CRUD)
✅ Configuration management
✅ Error handling best practices
✅ Web scraping and XML parsing
✅ Command-line argument processing
✅ Data validation and sanitization
✅ Logging and progress tracking

---

## 📈 Project Completion Status

- ✅ **Projects 1-7:** Fully implemented and tested
- ⏳ **Project 8:** OOPs/Inheritance structure (future enhancement)
- ✨ **Bonus:** Bulk insert capability added

**Overall Progress: ~85% Complete**

---

## 📄 License

Educational use only. Feel free to modify and extend.

---

## 🙌 Acknowledgments

Built as a comprehensive Python learning project demonstrating:
- Modern Python practices
- Database integration
- Web scraping techniques
- Configuration management
- Error handling patterns

---

**Last Updated:** April 25, 2026
**Status:** Production Ready for Learning ✅
**Total Scripts:** 12
**Total Lines of Code:** 2000+


