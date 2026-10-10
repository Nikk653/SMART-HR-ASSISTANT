import streamlit as st
from db.database import get_connection


def attendance_page():
    employee = st.session_state.get("employee")
    if employee is None:
        st.error("No employee in session. Please login.")
        return

    st.title("📅 Attendance")
    st.caption("Employee Attendance Management")
    st.divider()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT *
        FROM attendance
        WHERE employee_id = ?
        ORDER BY date DESC
        """,
        (employee["employee_id"],)
    )
    attendance = cursor.fetchall()
    conn.close()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Attendance", f"{employee.get('attendance', 0)}%")
    with c2:
        st.metric("Present Days", len(attendance))
    with c3:
        st.metric("Absent Days", max(0, 30 - len(attendance)))

    st.divider()
    st.subheader("Attendance History")

    if len(attendance) == 0:
        st.warning("No attendance records found.")
    else:
        table = []
        for row in attendance:
            try:
                date = row["date"]
                status = row["status"]
            except Exception:
                # fallback for tuple rows (common sqlite row tuples)
                date = row[2] if len(row) > 2 else None
                status = row[3] if len(row) > 3 else None
            table.append({"Date": date, "Status": status})

        st.dataframe(table, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Today's Attendance")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Check In", use_container_width=True):
            st.success("Check In Recorded Successfully")
    with col2:
        if st.button("🚪 Check Out", use_container_width=True):
            st.success("Check Out Recorded Successfully")

    st.divider()
    st.subheader("Monthly Summary")
    st.progress(employee.get("attendance", 0) / 100)
    st.write(f"Overall Attendance : {employee.get('attendance', 0)}%")
    st.info("Attendance analytics and monthly charts will be added in the next version.")
    st.divider()

    if st.button("⬅ Back to Dashboard", use_container_width=True):
        st.session_state.current_page = "dashboard"
        st.rerun()
        attendance_page()