from db.database import get_connection

conn = get_connection()
cursor = conn.cursor()

# =====================================================
# BRANCHES
# =====================================================

branches = [

("BR001","Delhi","India","Connaught Place, New Delhi","09:00 AM - 06:00 PM","HR001","PR001","IT001","AD001","SC001"),

("BR002","Mumbai","India","BKC Mumbai","09:00 AM - 06:00 PM","HR002","PR002","IT002","AD002","SC002"),

("BR003","Bengaluru","India","Electronic City","09:00 AM - 06:00 PM","HR003","PR003","IT003","AD003","SC003"),

("BR004","Hyderabad","India","HITEC City","09:00 AM - 06:00 PM","HR004","PR004","IT004","AD004","SC004"),

("BR005","Pune","India","Hinjewadi","09:00 AM - 06:00 PM","HR005","PR005","IT005","AD005","SC005")

]

cursor.executemany("""
INSERT OR IGNORE INTO branches
VALUES(?,?,?,?,?,?,?,?,?,?)
""", branches)

# =====================================================
# DEPARTMENTS
# =====================================================

departments = [

("D001","Artificial Intelligence"),

("D002","Human Resources"),

("D003","Finance"),

("D004","IT Support"),

("D005","Administration")

]

cursor.executemany("""
INSERT OR IGNORE INTO departments
VALUES(?,?)
""", departments)

# =====================================================
# ROLES
# =====================================================

roles = [

("R001","Employee"),

("R002","Manager"),

("R003","HR"),

("R004","Payroll"),

("R005","Admin")

]

cursor.executemany("""
INSERT OR IGNORE INTO roles
VALUES(?,?)
""", roles)

# =====================================================
# STAFF
# =====================================================

staff = [

("HR001","Anjali Verma","HR Manager","anjali@company.com","+91-9000000001","BR001"),
("HR002","Pooja Sharma","HR Manager","pooja@company.com","+91-9000000002","BR002"),
("HR003","Neha Kapoor","HR Manager","neha@company.com","+91-9000000003","BR003"),
("HR004","Ritika Jain","HR Manager","ritika@company.com","+91-9000000004","BR004"),
("HR005","Simran Kaur","HR Manager","simran@company.com","+91-9000000005","BR005"),

("IT001","Amit Singh","IT Manager","amit@company.com","+91-9111111111","BR001"),
("IT002","Vikas Sharma","IT Manager","vikas@company.com","+91-9111111112","BR002"),
("IT003","Rohan Gupta","IT Manager","rohan@company.com","+91-9111111113","BR003"),
("IT004","Sandeep Kumar","IT Manager","sandeep@company.com","+91-9111111114","BR004"),
("IT005","Deepak Verma","IT Manager","deepak@company.com","+91-9111111115","BR005"),

("PR001","Rakesh Mehta","Payroll Manager","rakesh@company.com","+91-9222222201","BR001"),
("PR002","Mohit Jain","Payroll Manager","mohit@company.com","+91-9222222202","BR002"),
("PR003","Tarun Singh","Payroll Manager","tarun@company.com","+91-9222222203","BR003"),
("PR004","Aakash Gupta","Payroll Manager","aakash@company.com","+91-9222222204","BR004"),
("PR005","Nitin Sharma","Payroll Manager","nitin@company.com","+91-9222222205","BR005")

]

cursor.executemany("""
INSERT OR IGNORE INTO staff
VALUES(?,?,?,?,?,?)
""", staff)

# =====================================================
# EMPLOYEES
# =====================================================

employees = [

("EMP001","12345","Nikhil","Kushwah","nikhil@company.com","+91-9876543210","India","English","BR001","D001","R001","2025-01-15",20,97.5,"Active"),

("EMP002","12345","Rahul","Sharma","rahul@company.com","+91-9876543211","India","Hindi","BR002","D002","R002","2024-06-10",18,95.0,"Active"),

("EMP003","12345","Priya","Verma","priya@company.com","+91-9876543212","India","English","BR003","D003","R001","2023-03-20",15,92.0,"Active"),

("EMP004","12345","Rohit","Gupta","rohit@company.com","+91-9876543213","India","English","BR004","D004","R001","2022-11-05",22,98.0,"Active"),

("EMP005","12345","Sneha","Kapoor","sneha@company.com","+91-9876543214","India","Hindi","BR005","D005","R003","2021-09-15",25,99.0,"Active")

]

cursor.executemany("""
INSERT OR IGNORE INTO employees
VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
""", employees)

# =====================================================
# PAYROLL
# =====================================================

payroll = [

("EMP001", 60000, 5000, 4000, 61000),
("EMP002", 55000, 4000, 3500, 55500),
("EMP003", 50000, 3000, 2500, 50500),
("EMP004", 65000, 6000, 5000, 66000),
("EMP005", 70000, 7000, 6000, 71000)

]

cursor.executemany(
"""
INSERT OR IGNORE INTO payroll
(employee_id, basic_salary, bonus, tax, net_salary)
VALUES (?, ?, ?, ?, ?)
""",
payroll
)

conn.commit()
conn.close()

print("=====================================")
print("Database Seed Completed Successfully")
print("Branches     : 5")
print("Departments  : 5")
print("Roles        : 5")
print("Staff        : 15")
print("Employees    : 5")
print("=====================================")