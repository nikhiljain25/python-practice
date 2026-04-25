# ✅ FIX: Root Access Denied - Recreate Container

## ❌ Problem

```
Access denied for user 'root'@'172.17.0.1'
```

**Why:** The password with special characters `#u2Fr!eRkwt*F6n` wasn't properly handled by the shell when creating the container.

---

## ✅ Solution: Recreate Container

### **Step 1: Stop and Remove Old Container**

```powershell
docker stop python_db
docker rm python_db
```

### **Step 2: Create New Container with Quoted Password**

Use this command (with password in quotes):

```powershell
docker run -d `
  --name python_db `
  -e "MYSQL_ROOT_PASSWORD=#u2Fr!eRkwt*F6n" `
  -e "MYSQL_DATABASE=freedb_python_mysql_db" `
  -e "MYSQL_USER=freedb_gavidi" `
  -e "MYSQL_PASSWORD=#u2Fr!eRkwt*F6n" `
  -p 3306:3306 `
  mysql:latest
```

### **Step 3: Wait 60 Seconds**

Let MySQL fully initialize.

### **Step 4: Verify Container**

```powershell
docker ps
```

Should show `python_db` running.

### **Step 5: Test Connection**

```powershell
docker exec -it python_db mysql -u root -p#u2Fr!eRkwt*F6n -e "SELECT 1"
```

Should output: `1`

---

## 🚀 Now Try Again

```bash
python python_practice_programs/project/mysql_table_creation.py
```

**Should work now!** ✅

---

## 📝 Your config.ini (Already Correct)

```ini
[mysql]
host = localhost
user = root
password = "#u2Fr!eRkwt*F6n"
database = freedb_python_mysql_db
port = 3306
```

No changes needed - just recreate the container!

---

**Status:** Container recreation guide provided  
**Action:** Follow steps above  
**Result:** Connection will succeed!

