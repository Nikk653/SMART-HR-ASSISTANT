from chatbot.knowledge_base import HR_KNOWLEDGE
from chatbot.leave import apply_leave
from db.database import get_connection


def get_response(intent, employee):

    # ==========================
    # Greeting
    # ==========================

    if intent == "greeting":

        return HR_KNOWLEDGE["greeting"]

    # ==========================
    # Leave Balance
    # ==========================

    if intent == "leave_balance":

        return f"""
📝 Leave Balance

You have {employee['leave_balance']} leaves remaining.
"""

    # ==========================
    # Apply Leave
    # ==========================

    if intent == "apply_leave":

        success = apply_leave(

            employee["employee_id"],

            "Tomorrow",

            "Applied through Smart HR Assistant"

        )

        if success:

            return """
✅ Leave Request Submitted Successfully

Leave Date : Tomorrow

Status : Pending

Your HR Manager will review your request.
"""

        return "Unable to submit leave request."

    # ==========================
    # Attendance
    # ==========================

    if intent == "attendance":

        return f"""
📅 Attendance

Attendance : {employee['attendance']}%
"""

    # ==========================
    # Profile
    # ==========================

    if intent == "profile":

        return f"""
👤 Employee Profile

Name : {employee['first_name']} {employee['last_name']}

Employee ID : {employee['employee_id']}

Email : {employee['email']}

Phone : {employee['phone']}

Branch : {employee['branch_name']}

Department : {employee['department_name']}

Role : {employee['role_name']}
"""

    # ==========================
    # Salary
    # ==========================

    if intent == "salary":

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(

            "SELECT * FROM payroll WHERE employee_id=?",

            (employee["employee_id"],)

        )

        salary = cursor.fetchone()

        conn.close()

        if salary:

            salary = dict(salary)

            return f"""
💰 Salary Details

Basic Salary : ₹{salary.get('basic_salary',0)}

Bonus : ₹{salary.get('bonus',0)}

Tax : ₹{salary.get('tax',0)}

Net Salary : ₹{salary.get('net_salary',0)}
"""

        return "Salary record not found."

        # ==========================
    # HR Manager
    # ==========================

    if intent == "hr":

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                s.name,
                s.email,
                s.phone
            FROM staff s
            JOIN branches b
            ON s.staff_id = b.hr_manager_id
            WHERE b.branch_id = ?
            """,
            (employee["branch_id"],)
        )

        hr = cursor.fetchone()

        conn.close()

        if hr:

            return f"""
👨‍💼 HR Manager

Name : {hr['name']}

Email : {hr['email']}

Phone : {hr['phone']}
"""

        return "HR Manager information not found."

    # ==========================
    # Knowledge Base
    # ==========================

    if intent == "leave_policy":
        return HR_KNOWLEDGE["leave_policy"]

    if intent == "working_hours":
        return HR_KNOWLEDGE["working_hours"]

    if intent == "office_timing":
        return HR_KNOWLEDGE["office_timing"]

    if intent == "holiday":
        return HR_KNOWLEDGE["holiday"]

    if intent == "company_policy":
        return HR_KNOWLEDGE["company_policy"]

    if intent == "dress_code":
        return HR_KNOWLEDGE["dress_code"]

    if intent == "wfh":
        return HR_KNOWLEDGE["wfh"]

    if intent == "training":
        return HR_KNOWLEDGE["training"]

    if intent == "bonus":
        return HR_KNOWLEDGE["bonus"]

    if intent == "tax":
        return HR_KNOWLEDGE["tax"]

    if intent == "pf":
        return HR_KNOWLEDGE["pf"]

    if intent == "goodbye":
        return HR_KNOWLEDGE["goodbye"]

    # ==========================
    # Default Response
    # ==========================

    return """
❌ Sorry!

I couldn't understand your question.

You can ask things like:

• Show my salary
• Show my attendance
• How many leaves do I have?
• Apply leave tomorrow
• Who is my HR?
• Show my profile
• Office timing
• Company policy
"""