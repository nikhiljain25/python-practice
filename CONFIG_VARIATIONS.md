# 🔧 PROJECT 5 - CONFIG.INI VARIATIONS

## Original Config (Remote MySQL)

**File:** `config/config.ini`

### For Remote MySQL (sql.freedb.tech)
```ini
[mysql]
host = sql.freedb.tech
user = freedb_gavidi
password = "#u2Fr!eRkwt*F6n"
database = freedb_python_mysql_db
port = 3306
```

---

## Updated Config (Local Docker MySQL)

### For Local Docker MySQL
```ini
[mysql]
host = localhost
user = root
password = root123
database = project5_db
port = 3306
```

**Setup Command:**
```bash
docker run -d \
  --name python_db \
  -e MYSQL_ROOT_PASSWORD="#u2Fr!eRkwt*F6n" \
  -e MYSQL_DATABASE=project5_db \
  -p 3306:3306 \
  mysql:latest
```

---

## Alternative Config (Custom Docker Port)

### For Custom Port (3307 instead of 3306)
```ini
[mysql]
host = localhost
user = root
password = root123
database = project5_db
port = 3307
```

**Setup Command:**
```bash
docker run -d \
  --name mysql-project5 \
  -e MYSQL_ROOT_PASSWORD=root123 \
  -e MYSQL_DATABASE=project5_db \
  -p 3307:3306 \
  mysql:latest
```

---

## SQLElectron Connection Settings

### To Connect SQLElectron to Docker MySQL

**Connection Configuration:**
```
Connection Name: Local MySQL Project5
Database Type: MySQL
Server Address: localhost
Port: 3306 (or 3307 if using custom port)
Username: root
Password: root123
Database: project5_db
SSH: (leave unchecked)
```

---

## COMPLETE CONFIG.INI TEMPLATE

Below is the complete `config.ini` file with LOCAL MySQL settings:

```ini
[search]
search_0 = 2. What happens to the
search_1 = 4. At what temperature
search_2 = 10. Which state of
search_3 = 7. Which of the following statements best describes a liquid?
search_4 = 8.
search_5 = 9.
search_6 = 1.
search_7 = 3.
search_8 = 5.
search_9 = 6.

[regex]
question_answer_pattern = \d+\.\s*(.*?)\n.*?Answer:\s*([A-D]\)\s*.*)

[mysql]
host = localhost
user = root
password = root123
database = project5_db
port = 3306
select_query_1 = SELECT * FROM questions
insert_query_1 = INSERT INTO questions (question, answer) VALUES
create_query_1 = CREATE TABLE IF NOT EXISTS questions ( id INT AUTO_INCREMENT PRIMARY KEY, question TEXT, answer TEXT )
delete_query_1 = TRUNCATE TABLE questions

[files]
input_file = ../../content/Chemistry Questions.pdf
output_file = ../../content/output.txt
file_path = ../../content/
output_url_content = ../../content/output_url_content.txt

[urls]
rss_url = https://www.w3schools.com/xml/xml_rss.asp
```

**Key Changes for Local MySQL:**
- `host = localhost` (was sql.freedb.tech)
- `user = root` (was freedb_gavidi)
- `password = root123` (was #u2Fr!eRkwt*F6n)
- `database = project5_db` (was freedb_python_mysql_db)
- `port = 3306` (same)

---

## How to Apply This Config

### Step 1: Locate config.ini
```
D:\Study_Material\GenAI\practice program\
python_practice_programs\
config\
config.ini  ← Edit this file
```

### Step 2: Open with Text Editor
- Right-click on `config.ini`
- Select "Open with" → Notepad (or your editor)

### Step 3: Replace [mysql] Section
Find this section:
```ini
[mysql]
host = sql.freedb.tech
user = freedb_gavidi
password = "#u2Fr!eRkwt*F6n"
database = freedb_python_mysql_db
port = 3306
```

Replace with:
```ini
[mysql]
host = localhost
user = root
password = root123
database = project5_db
port = 3306
```

### Step 4: Save File
- Press Ctrl+S or File → Save
- Close editor

### Step 5: Test Connection
```bash
cd "D:\Study_Material\GenAI\practice program"
python python_practice_programs/project/mysql_connection.py
```

**Expected Output:**
```
✓ Successfully connected to LOCAL MySQL!
```

---

## Configuration Comparison Table

| Setting | Remote (Original) | Local Docker |
|---------|------------------|--------------|
| host | sql.freedb.tech | localhost |
| user | freedb_gavidi | root |
| password | #u2Fr!eRkwt*F6n | root123 |
| database | freedb_python_mysql_db | project5_db |
| port | 3306 | 3306 |
| Connection | Internet required | Local only |
| Speed | Slower | Faster |
| Control | No | Yes |

---

## Docker Command Reference

### Start MySQL Container
```bash
docker run -d --name mysql-project5 -e MYSQL_ROOT_PASSWORD=root123 -e MYSQL_DATABASE=project5_db -p 3306:3306 mysql:latest
```

### Check Container Status
```bash
docker ps
```

### View Container Logs
```bash
docker logs mysql-project5
```

### Stop Container
```bash
docker stop mysql-project5
```

### Start Container Again
```bash
docker start mysql-project5
```

### Delete Container
```bash
docker rm mysql-project5
```

### Access MySQL Console in Docker
```bash
docker exec -it mysql-project5 mysql -u root -proot123 project5_db
```

### Reset Database (Delete & Recreate)
```bash
docker stop mysql-project5
docker rm mysql-project5
docker run -d --name mysql-project5 -e MYSQL_ROOT_PASSWORD=root123 -e MYSQL_DATABASE=project5_db -p 3306:3306 mysql:latest
```

---

## Environment Variable Approach (Advanced)

Instead of hardcoding in config.ini, you can use environment variables:

### Create .env File
File: `D:\Study_Material\GenAI\practice program\.env`
```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=root123
MYSQL_DATABASE=project5_db
MYSQL_PORT=3306
```

### Update config.ini to Use Environment Variables
```ini
[mysql]
host = ${MYSQL_HOST}
user = ${MYSQL_USER}
password = ${MYSQL_PASSWORD}
database = ${MYSQL_DATABASE}
port = ${MYSQL_PORT}
```

### Update read_config.py to Read Environment Variables
```python
import os
from dotenv import load_dotenv

load_dotenv()

def get_config_value(section, key):
    # First try environment variable
    env_key = f"{section}_{key}".upper()
    if os.getenv(env_key):
        return os.getenv(env_key)
    
    # Then try config.ini
    # ... existing code ...
```

**Benefits:**
- More secure (don't hardcode passwords)
- Easy to switch between environments
- Works with CI/CD systems

---

## Quick Decision Guide

### Choose Based On Your Need:

**"I want quick setup"**
→ Use Docker with config.ini changes above

**"I want more security"**
→ Use environment variables approach

**"I want visual management"**
→ Use SQLElectron with Docker

**"I want to go back to remote"**
→ Switch config.ini back to original values

---

## Troubleshooting Connection Issues

### Test 1: Docker Container Running?
```bash
docker ps
# Should show mysql-project5 container
```

### Test 2: Port 3306 Available?
```bash
netstat -ano | findstr :3306
# If shows process, stop it or use different port
```

### Test 3: MySQL Password Correct?
```bash
docker exec -it mysql-project5 mysql -u root -proot123 -e "SELECT 1"
# Should show: 1
```

### Test 4: Database Exists?
```bash
docker exec -it mysql-project5 mysql -u root -proot123 -e "SHOW DATABASES;"
# Should show: project5_db
```

### Test 5: Python Connection?
```python
import mysql.connector
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="project5_db"
)
print("Connected!" if conn.is_connected() else "Failed!")
```

---

## Summary

To use your Docker MySQL with this project:

1. **Start Docker container** with the command provided
2. **Update config.ini** with local credentials
3. **Test connection** with Python
4. **Use SQLElectron** to view data visually
5. **Run Project 5** commands normally

Everything else stays the same! 🎉

---

**Configuration Status:** ✅ READY  
**Docker Status:** ✅ DOCUMENTED  
**SQLElectron Status:** ✅ CONFIGURED  

**You're all set to use local MySQL with your project!**

