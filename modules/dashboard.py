import streamlit as st


def dashboard_page():
    """Compact professional enterprise dashboard."""

    employee = st.session_state.get("employee")

    if not employee:
        st.error("Employee information is not available.")
        return

    def get_value(key, default: str | int | float | None = "N/A"):
        value = employee.get(key, default)
        return default if value is None or value == "" else value

    first_name = str(get_value("first_name", "Employee"))
    last_name = str(get_value("last_name", ""))
    full_name = f"{first_name} {last_name}".strip()

    employee_id = str(get_value("employee_id"))
    department = str(get_value("department_name"))
    role = str(get_value("role_name"))
    branch = str(get_value("branch_name"))
    status = str(get_value("status", "Active"))
    leave_balance = str(get_value("leave_balance", 0))
    attendance = str(get_value("attendance", 0))
    joining_date = str(get_value("joining_date"))
    email = str(get_value("email"))
    phone = str(get_value("phone"))

    # ---------------------------------------------------------
    # Compact enterprise styling
    # ---------------------------------------------------------
    st.markdown(
        """
        <style>
        /* Main workspace */
        .block-container {
            max-width: 1260px;
            padding: 1.05rem 1.35rem 2rem 1.35rem;
        }

        .stApp {
            background: #f4f6f9;
        }

        /* Make the sidebar narrower */
        [data-testid="stSidebar"] {
            min-width: 250px;
            max-width: 270px;
        }

        /* Sidebar spacing */
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            gap: 0.45rem;
        }

        /* Markdown headings */
        .block-container h1 {
            font-size: 30px !important;
            line-height: 1.15 !important;
            margin: 0.15rem 0 0.3rem 0 !important;
            color: #172033;
        }

        .block-container h2 {
            font-size: 20px !important;
            line-height: 1.25 !important;
            margin: 1.15rem 0 0.7rem 0 !important;
            color: #172033;
        }

        .block-container h3 {
            font-size: 16px !important;
            margin: 0.6rem 0 0.35rem 0 !important;
        }

        /* Captions */
        .block-container .stCaption {
            font-size: 12px !important;
            color: #667085 !important;
        }

        /* Metrics */
        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #e1e6ed;
            border-radius: 12px;
            padding: 13px 15px;
            min-height: 94px;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.025);
        }

        div[data-testid="stMetricLabel"] {
            font-size: 11px !important;
            color: #667085 !important;
        }

        div[data-testid="stMetricValue"] {
            font-size: 22px !important;
            line-height: 1.1 !important;
            color: #172033 !important;
            font-weight: 750 !important;
        }

        div[data-testid="stMetricDelta"] {
            font-size: 10px !important;
        }

        /* Native bordered cards */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: #ffffff;
            border-color: #e1e6ed !important;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.02);
        }

        /* Buttons */
        div.stButton > button {
            min-height: 40px;
            border-radius: 8px !important;
            font-size: 13px !important;
        }

        /* Reduce default divider whitespace */
        hr {
            margin: 0.65rem 0 !important;
        }

        /* Small muted helper text */
        .muted {
            color: #667085;
            font-size: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------------
    # Compact page header
    # ---------------------------------------------------------
    top_left, top_right = st.columns([4, 1.15], gap="large")

    with top_left:
        st.caption("EMPLOYEE SELF-SERVICE PORTAL")
        st.title(f"Welcome back, {first_name}")
        st.caption(
            "Manage your employee information and access HR services."
        )

    with top_right:
        with st.container(border=True):
            st.caption("EMPLOYEE ID")
            st.markdown(f"### {employee_id}")
            st.caption(full_name)

    st.divider()

    # ---------------------------------------------------------
    # HR Overview
    # ---------------------------------------------------------
    st.markdown("## HR Overview")

    c1, c2, c3, c4 = st.columns(4, gap="medium")

    with c1:
        st.metric("Leave Balance", f"{leave_balance} Days")

    with c2:
        st.metric("Attendance", f"{attendance}%")

    with c3:
        st.metric("Employment Status", status)

    with c4:
        st.metric("Work Location", branch)

    # ---------------------------------------------------------
    # Employee Information
    # ---------------------------------------------------------
    st.markdown("## Employee Information")

    with st.container(border=True):
        r1 = st.columns(3, gap="large")

        with r1[0]:
            st.caption("EMPLOYEE")
            st.write(f"**{full_name}**")

        with r1[1]:
            st.caption("ROLE")
            st.write(f"**{role}**")

        with r1[2]:
            st.caption("DEPARTMENT")
            st.write(f"**{department}**")

        st.divider()

        r2 = st.columns(3, gap="large")

        with r2[0]:
            st.caption("JOINING DATE")
            st.write(f"**{joining_date}**")

        with r2[1]:
            st.caption("EMAIL")
            st.write(f"**{email}**")

        with r2[2]:
            st.caption("PHONE")
            st.write(f"**{phone}**")

    # ---------------------------------------------------------
    # HR Assistant
    # ---------------------------------------------------------
    st.markdown("## Smart HR Assistant")

    with st.container(border=True):
        st.info(
            "Ask about leave, attendance, payroll, company policies, "
            "workplace procedures and other HR services. Sensitive or "
            "complex concerns can be escalated to human HR."
        )

        a1, a2, a3 = st.columns(3, gap="medium")

        with a1:
            if st.button(
                "Open HR Assistant",
                use_container_width=True,
                key="dashboard_open_chat",
            ):
                st.info("Select **Chatbot** from the sidebar.")

        with a2:
            if st.button(
                "View Leave",
                use_container_width=True,
                key="dashboard_open_leave",
            ):
                st.info("Select **Leave** from the sidebar.")

        with a3:
            if st.button(
                "View Attendance",
                use_container_width=True,
                key="dashboard_open_attendance",
            ):
                st.info("Select **Attendance** from the sidebar.")

    st.caption(
        "Smart HR Assistant • Secure employee self-service • Authorized access only"
    )
