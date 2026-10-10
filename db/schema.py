from db.database import get_connection

# ===============================
# Create Database Connection
# ===============================

conn = get_connection()
cursor = conn.cursor()

# ==========================================
# Employees Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(

employee_id TEXT PRIMARY KEY,

password TEXT NOT NULL,

first_name TEXT NOT NULL,

last_name TEXT,

email TEXT UNIQUE,

phone TEXT,

country TEXT,

language TEXT,

branch_id TEXT,

department_id TEXT,

role_id TEXT,

joining_date TEXT,

leave_balance INTEGER DEFAULT 20,

attendance REAL DEFAULT 100,

status TEXT DEFAULT 'Active'

)
""")

# ==========================================
# Branches Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS branches(

branch_id TEXT PRIMARY KEY,

branch_name TEXT NOT NULL,

country TEXT,

address TEXT,

working_hours TEXT,

hr_manager_id TEXT,

payroll_manager_id TEXT,

it_manager_id TEXT,

admin_manager_id TEXT,

security_head_id TEXT

)
""")

# ==========================================
# Staff Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS staff(

staff_id TEXT PRIMARY KEY,

name TEXT,

role TEXT,

email TEXT,

phone TEXT,

branch_id TEXT

)
""")

# ==========================================
# Departments Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS departments(

department_id TEXT PRIMARY KEY,

department_name TEXT

)
""")

# ==========================================
# Roles Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS roles(

role_id TEXT PRIMARY KEY,

role_name TEXT

)
""")

# ==========================================
# Leave Requests Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS leave_requests(

leave_id INTEGER PRIMARY KEY AUTOINCREMENT,

employee_id TEXT,

leave_type TEXT,

from_date TEXT,

to_date TEXT,

reason TEXT,

status TEXT

)
""")

# ==========================================
# Attendance Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(

attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,

employee_id TEXT,

date TEXT,

status TEXT

)
""")

# ==========================================
# Payroll Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS payroll(

payroll_id INTEGER PRIMARY KEY AUTOINCREMENT,

employee_id TEXT,

basic_salary REAL,

bonus REAL,

tax REAL,

net_salary REAL

)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    employee_id TEXT NOT NULL,

    question TEXT NOT NULL,

    answer TEXT NOT NULL,

    intent TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(employee_id)
    REFERENCES employees(employee_id)

)
""")

# ==========================================
# Tickets Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets(

ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,

employee_id TEXT,

department TEXT,

issue TEXT,

priority TEXT,

status TEXT

)
""")

# ==========================================
# Announcements Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS announcements(

announcement_id INTEGER PRIMARY KEY AUTOINCREMENT,

title TEXT,

description TEXT,

branch_id TEXT,

date TEXT

)
""")

# ==========================================
# Chat History Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history(

chat_id INTEGER PRIMARY KEY AUTOINCREMENT,

employee_id TEXT,

user_query TEXT,

bot_response TEXT,

timestamp TEXT

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS leave_requests(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    employee_id TEXT NOT NULL,

    leave_date TEXT NOT NULL,

    reason TEXT,

    status TEXT DEFAULT 'Pending',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(employee_id)
    REFERENCES employees(employee_id)

)
""")


# ==========================================
# Save Changes
# ==========================================

conn.commit()
conn.close()

print("✅ Database & All Tables Created Successfully")