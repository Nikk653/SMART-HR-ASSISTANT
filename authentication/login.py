import streamlit as st

from authentication.auth import login_user
from authentication.session import create_session


def login_page():
    """Stable professional login page for Smart HR Assistant."""

    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at 10% 15%, rgba(37,99,235,.16), transparent 25%),
                radial-gradient(circle at 90% 80%, rgba(14,165,233,.10), transparent 25%),
                linear-gradient(135deg, #071321 0%, #0b203c 52%, #07111f 100%);
        }

        .block-container {
            max-width: 900px;
            padding-top: 3rem;
            padding-bottom: 2rem;
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        .brand {
            text-align: center;
            margin-bottom: 28px;
        }

        .brand-mark {
            width: 56px;
            height: 56px;
            margin: 0 auto 12px auto;
            border-radius: 15px;
            background: linear-gradient(135deg, #2563eb, #38bdf8);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 17px;
            box-shadow: 0 10px 24px rgba(37,99,235,.25);
        }

        .brand-title {
            color: #f8fafc;
            font-size: 31px;
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        .brand-subtitle {
            color: #9fb0c5;
            font-size: 14px;
            margin-top: 5px;
        }

        .eyebrow {
            color: #60a5fa;
            font-size: 11px;
            font-weight: 750;
            letter-spacing: .10em;
            text-transform: uppercase;
            margin-bottom: 7px;
        }

        .login-title {
            color: #f8fafc;
            font-size: 27px;
            font-weight: 780;
            margin-bottom: 5px;
        }

        .login-description {
            color: #9fb0c5;
            font-size: 13px;
            line-height: 1.6;
            margin-bottom: 18px;
        }

        .secure-note {
            color: #7f93aa;
            font-size: 11px;
            text-align: center;
            margin-top: 16px;
        }

        .footer {
            color: #64748b;
            font-size: 11px;
            text-align: center;
            margin-top: 18px;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(12, 27, 46, 0.94);
            border: 1px solid rgba(148,163,184,.16);
            border-radius: 18px;
            box-shadow: 0 18px 45px rgba(0,0,0,.24);
        }

        div[data-testid="stTextInput"] label {
            color: #dbe5f2;
            font-size: 13px;
            font-weight: 650;
        }

        div[data-testid="stTextInput"] input {
            min-height: 46px;
            border-radius: 10px;
            border: 1px solid #334155;
            background: #091729;
            color: #f8fafc;
        }

        div[data-testid="stTextInput"] input::placeholder {
            color: #708197;
        }

        div[data-testid="stTextInput"] input[aria-label="Employee ID"] {
            text-transform: uppercase;
        }

        div[data-testid="stTextInput"] input:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 1px #3b82f6;
        }

        div.stFormSubmitButton > button {
            min-height: 46px;
            border-radius: 10px !important;
            background: linear-gradient(90deg, #2563eb, #1d4ed8) !important;
            border: 1px solid #2563eb !important;
            color: #fff !important;
            font-weight: 750 !important;
        }

        div.stFormSubmitButton > button:hover {
            background: linear-gradient(90deg, #3b82f6, #2563eb) !important;
            border-color: #3b82f6 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">HR</div>
            <div class="brand-title">Smart HR Assistant</div>
            <div class="brand-subtitle">Employee Self-Service Portal</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([1, 1.15, 1])

    with center:
        with st.container(border=True):
            st.markdown(
                '<div class="eyebrow">Secure Employee Access</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="login-title">Employee Login</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="login-description">'
                'Sign in with your employee credentials to access the HR portal.'
                '</div>',
                unsafe_allow_html=True,
            )

            # Enter key submits this form.
            with st.form("employee_login_form", clear_on_submit=False):
                employee_id = st.text_input(
                    "Employee ID",
                    placeholder="EMP001",
                    autocomplete="username",
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter password",
                    autocomplete="current-password",
                )

                submitted = st.form_submit_button(
                    "Sign In",
                    use_container_width=True,
                )

            if submitted:
                employee_id = employee_id.strip().upper()
                password = password.strip()

                if not employee_id or not password:
                    st.warning("Please enter Employee ID and Password.")
                    return

                user = login_user(employee_id, password)

                if user:
                    # login_user() currently returns sqlite3.Row.
                    # sqlite3.Row supports [] access, not .get().
                    first_name = (
                        user["first_name"]
                        if "first_name" in user.keys()
                        else "Employee"
                    )

                    create_session(user)

                    st.success(f"Welcome back, {first_name}.")
                    st.rerun()

                else:
                    st.error("Invalid Employee ID or Password.")

            st.markdown(
                '<div class="secure-note">'
                '🔒 Secure authenticated access • Never share your password'
                '</div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="footer">'
        'Smart HR Assistant • Employee Self-Service Portal • © 2026'
        '</div>',
        unsafe_allow_html=True,
    )
