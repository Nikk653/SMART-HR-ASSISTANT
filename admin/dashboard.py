import streamlit as st

from admin.employees import employees_page
from admin.leaves import leaves_page
from admin.payroll import payroll_page
from admin.analytics import analytics_page


def admin_dashboard():

    st.title("👨‍💼 HR Admin Panel")

    page = st.sidebar.radio(

        "Admin Menu",

        [

            "Employees",

            "Leave Requests",

            "Payroll",

            "Analytics"

        ]

    )

    if page == "Employees":

        employees_page()

    elif page == "Leave Requests":

        leaves_page()

    elif page == "Payroll":

        payroll_page()

    else:

        analytics_page()