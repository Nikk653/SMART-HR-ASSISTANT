import streamlit as st
from db.database import get_connection


def payroll_page():

    employee = st.session_state.employee

    st.title("💰 Payroll")

    st.caption("Employee Salary Management")

    st.divider()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            basic_salary,
            bonus,
            tax,
            net_salary
        FROM payroll
        WHERE employee_id = ?
        ORDER BY payroll_id DESC
        LIMIT 1
        """,
        (employee["employee_id"],)
    )

    salary = cursor.fetchone()

    conn.close()

    if salary is None:

        st.warning("No Salary Record Found.")

        return

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Basic Salary",
            f"₹ {salary['basic_salary']:,.0f}"
        )

    with c2:

        st.metric(
            "Bonus",
            f"₹ {salary['bonus']:,.0f}"
        )

    with c3:

        st.metric(
            "Tax",
            f"₹ {salary['tax']:,.0f}"
        )

    with c4:

        st.metric(
            "Net Salary",
            f"₹ {salary['net_salary']:,.0f}"
        )

    st.divider()

    st.subheader("💳 Salary Details")

    st.write(f"**Employee ID :** {employee['employee_id']}")
    st.write(f"**Employee Name :** {employee['first_name']} {employee['last_name']}")
    st.write(f"**Department :** {employee['department_name']}")
    st.write(f"**Role :** {employee['role_name']}")

    st.divider()

    st.subheader("📊 Salary Breakdown")

    breakdown = [
        {
            "Component": "Basic Salary",
            "Amount": f"₹ {salary['basic_salary']:,.0f}"
        },
        {
            "Component": "Bonus",
            "Amount": f"₹ {salary['bonus']:,.0f}"
        },
        {
            "Component": "Tax",
            "Amount": f"₹ {salary['tax']:,.0f}"
        },
        {
            "Component": "Net Salary",
            "Amount": f"₹ {salary['net_salary']:,.0f}"
        }
    ]

    st.dataframe(
        breakdown,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("📄 Payslip")

    st.info(
        "PDF Payslip download will be available in the next version."
    )

    st.button(
        "⬇ Download Payslip",
        use_container_width=True,
        disabled=True
    )

    st.divider()

    st.subheader("📈 Salary Insights")

    st.success("✔ Salary Credited Successfully")

    st.info("💡 Performance Bonus Eligible")

    st.warning("🧾 Income Tax Deducted")

    st.divider()

    if st.button(
        "⬅ Back to Dashboard",
        use_container_width=True
    ):

        st.session_state.current_page = "dashboard"

        st.rerun()
        payroll_page()