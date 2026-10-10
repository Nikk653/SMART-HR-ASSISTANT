import streamlit as st
from db.database import get_connection
from datetime import date


def leave_page():

    employee = st.session_state.employee

    st.title("🌴 Leave Management")

    st.caption("Apply and Track Your Leave Requests")

    st.divider()

    st.metric(
        "Remaining Leave",
        f"{employee['leave_balance']} Days"
    )

    st.divider()

    st.subheader("📝 Apply Leave")

    leave_type = st.selectbox(

        "Leave Type",

        [

            "Casual Leave",

            "Sick Leave",

            "Earned Leave",

            "Work From Home"

        ]

    )

    from_date = st.date_input(

        "From Date",

        date.today()

    )

    to_date = st.date_input(

        "To Date",

        date.today()

    )

    reason = st.text_area(

        "Reason"

    )

    if st.button(

        "Submit Leave Request",

        use_container_width=True

    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        INSERT INTO leave_requests(

        employee_id,

        leave_type,

        from_date,

        to_date,

        reason,

        status

        )

        VALUES(?,?,?,?,?,?)

        """,

        (

            employee["employee_id"],

            leave_type,

            str(from_date),

            str(to_date),

            reason,

            "Pending"

        )

        )

        conn.commit()

        conn.close()

        st.success(

            "Leave Request Submitted Successfully."

        )

        st.rerun()

    st.divider()

    st.subheader("📋 Leave History")

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            leave_type,
            from_date,
            to_date,
            reason,
            status
        FROM leave_requests
        WHERE employee_id = ?
        ORDER BY leave_id DESC
        """,
        (employee["employee_id"],)
    )

    leaves = cursor.fetchall()

    conn.close()

    if len(leaves) == 0:

        st.warning("No Leave Requests Found.")

    else:

        table = []

        pending = 0
        approved = 0
        rejected = 0

        for leave in leaves:

            table.append(
                {
                    "Leave Type": leave["leave_type"],
                    "From": leave["from_date"],
                    "To": leave["to_date"],
                    "Reason": leave["reason"],
                    "Status": leave["status"]
                }
            )

            if leave["status"] == "Pending":
                pending += 1

            elif leave["status"] == "Approved":
                approved += 1

            elif leave["status"] == "Rejected":
                rejected += 1

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Pending", pending)

        with c2:
            st.metric("Approved", approved)

        with c3:
            st.metric("Rejected", rejected)

    st.divider()

    st.subheader("📌 Leave Policy")

    st.info(
        """
• Casual Leave : 12 Days

• Sick Leave : 8 Days

• Earned Leave : Company Policy

• Work From Home : Manager Approval Required
        """
    )

    st.divider()

    if st.button(
        "⬅ Back to Dashboard",
        use_container_width=True
    ):

        st.session_state.current_page = "dashboard"

        st.rerun()
        leave_page()