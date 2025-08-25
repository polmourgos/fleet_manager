# Fleet Manager - Data Import Templates

## 🚗 Bulk Import Scripts

### Drivers Import Template
```python
# drivers_import.py
import sqlite3
import csv

def import_drivers_from_csv(csv_file, db_path="fleet.db"):
    """Import drivers from CSV file"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT INTO drivers (name, surname, notes) 
                VALUES (?, ?, ?)
            """, (row['name'], row['surname'], row.get('notes', '')))
    
    conn.commit()
    conn.close()
    print(f"Imported drivers from {csv_file}")

# Usage: python drivers_import.py
```

### Vehicles Import Template
```python
# vehicles_import.py
import sqlite3
import csv

def import_vehicles_from_csv(csv_file, db_path="fleet.db"):
    """Import vehicles from CSV file"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT INTO vehicles (plate, brand, vtype, purpose) 
                VALUES (?, ?, ?, ?)
            """, (row['plate'], row.get('brand', ''), 
                  row.get('vtype', ''), row.get('purpose', '')))
    
    conn.commit()
    conn.close()
    print(f"Imported vehicles from {csv_file}")

# Usage: python vehicles_import.py
```

## 📋 CSV Templates

### drivers_template.csv
```csv
name,surname,notes
Γιάννης,Παπαδόπουλος,Οδηγός Α' κατηγορίας
Μαρία,Κωνσταντίνου,Οδηγός Β' κατηγορίας
...
```

### vehicles_template.csv
```csv
plate,brand,vtype,purpose
ΑΒΓ-1234,Toyota,Επιβατικό,Υπηρεσιακό
ΔΕΖ-5678,Mercedes,Φορτηγό,Μεταφορές
...
```

## 🔧 Migration Scripts

### Database Backup Before Import
```python
# backup_before_import.py
import shutil
from datetime import datetime

def backup_database():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2("fleet.db", f"fleet_backup_{timestamp}.db")
    print(f"Backup created: fleet_backup_{timestamp}.db")

backup_database()
```

### Data Validation Script
```python
# validate_import.py
import sqlite3

def validate_data():
    conn = sqlite3.connect("fleet.db")
    cursor = conn.cursor()
    
    # Check drivers
    cursor.execute("SELECT COUNT(*) FROM drivers")
    drivers_count = cursor.fetchone()[0]
    print(f"Total drivers: {drivers_count}")
    
    # Check vehicles  
    cursor.execute("SELECT COUNT(*) FROM vehicles")
    vehicles_count = cursor.fetchone()[0]
    print(f"Total vehicles: {vehicles_count}")
    
    # Check for duplicates
    cursor.execute("SELECT plate, COUNT(*) FROM vehicles GROUP BY plate HAVING COUNT(*) > 1")
    duplicates = cursor.fetchall()
    if duplicates:
        print(f"Duplicate plates found: {duplicates}")
    else:
        print("No duplicate plates found")
    
    conn.close()

validate_data()
```

---

**📝 Instructions:**
1. Create CSV files using the templates above
2. Fill with your data (30 drivers, 40 vehicles)
3. Run backup script first
4. Run import scripts
5. Validate data integrity
