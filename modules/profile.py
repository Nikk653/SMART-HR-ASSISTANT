import streamlit as st


def profile_page():
    """
    Professional employee profile page for Smart HR Assistant.

    Uses employee data stored in:
        st.session_state["employee"]

    This page intentionally does NOT display passwords or other
    authentication credentials.
    """

    employee = st.session_state.get("employee")

    if not employee:
        st.error("Employee information is not available.")
        return

    # ---------------------------------------------------------
    # Helper
    # ---------------------------------------------------------
    def value(key, default: str | int | float | None = "N/A") -> str:
        result = employee.get(key, default)
        if result is None or result == "":
            return str(default)
        return str(result)

    # ---------------------------------------------------------
    # Employee data
    # ---------------------------------------------------------
    first_name = value("first_name", "")
    last_name = value("last_name", "")
    full_name = f"{first_name} {last_name}".strip()

    if not full_name:
        full_name = "Employee"

    employee_id = value("employee_id")
    department = value("department_name")
    role = value("role_name")
    branch = value("branch_name")
    joining_date = value("joining_date")
    email = value("email")
    phone = value("phone")
    country = value("country")
    language = value("language")
    status = value("status", "Active")
    leave_balance = value("leave_balance", 0)
    attendance = value("attendance", 0)
    employment_type = value("employment_type", "Full Time")
    work_mode = value("work_mode", "Hybrid")
    reporting_manager = value("reporting_manager", "HR Manager")
    emergency_name = value("emergency_contact_name", "Family Member")
    emergency_relation = value("emergency_contact_relation", "Father")
    emergency_phone = value("emergency_contact_phone", "+91-9000000000")

    raw_skills = employee.get("skills")
    if isinstance(raw_skills, str):
        skills = [s.strip() for s in raw_skills.split(",") if s.strip()]
    elif isinstance(raw_skills, (list, tuple)):
        skills = [str(s).strip() for s in raw_skills if str(s).strip()]
    else:
        skills = [
            "Python",
            "Machine Learning",
            "Artificial Intelligence",
            "SQL",
            "Streamlit",
            "NLP",
        ]

    # ---------------------------------------------------------
    # Page CSS
    # ---------------------------------------------------------
    st.markdown(
        """
        <style>
        .profile-hero {
            padding: 26px 28px;
            border-radius: 18px;
            background: linear-gradient(135deg, #172554 0%, #1d4ed8 100%);
            color: white;
            margin-bottom: 22px;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.12);
        }

        .avatar {
            width: 78px;
            height: 78px;
            border-radius: 50%;
            background: rgba(255,255,255,0.18);
            border: 1px solid rgba(255,255,255,0.28);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            font-weight: 700;
            color: white;
            margin-bottom: 12px;
        }

        .hero-name {
            font-size: 30px;
            font-weight: 750;
            line-height: 1.15;
            margin-bottom: 5px;
        }

        .hero-subtitle {
            font-size: 15px;
            opacity: 0.9;
            margin-bottom: 12px;
        }

        .hero-pill {
            display: inline-block;
            padding: 5px 11px;
            border-radius: 999px;
            background: rgba(255,255,255,0.16);
            border: 1px solid rgba(255,255,255,0.22);
            font-size: 13px;
        }

        .section-title {
            font-size: 21px;
            font-weight: 700;
            margin-top: 18px;
            margin-bottom: 12px;
        }

        .info-card {
            padding: 16px 18px;
            border: 1px solid rgba(148,163,184,0.25);
            border-radius: 14px;
            background: rgba(248,250,252,0.75);
            margin-bottom: 12px;
            min-height: 82px;
        }

        .info-label {
            font-size: 12px;
            color: #64748b;
            margin-bottom: 5px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }

        .info-value {
            font-size: 15px;
            color: #0f172a;
            font-weight: 650;
            word-break: break-word;
        }

        .metric-card {
            padding: 18px;
            border: 1px solid rgba(148,163,184,0.25);
            border-radius: 14px;
            background: rgba(248,250,252,0.75);
            text-align: center;
            margin-bottom: 10px;
        }

        .metric-label {
            color: #64748b;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }

        .metric-value {
            color: #0f172a;
            font-size: 27px;
            font-weight: 750;
            margin-top: 5px;
        }

        .skill {
            display: inline-block;
            padding: 6px 11px;
            margin: 0 6px 7px 0;
            border-radius: 999px;
            background: #dbeafe;
            color: #1d4ed8;
            font-size: 12px;
            font-weight: 650;
        }

        .doc-card {
            padding: 18px;
            border: 1px solid rgba(148,163,184,0.25);
            border-radius: 14px;
            background: rgba(248,250,252,0.75);
            text-align: center;
            min-height: 145px;
        }

        .doc-icon {
            font-size: 30px;
            margin-bottom: 4px;
        }

        .small-muted {
            color: #64748b;
            font-size: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------------
    # Header
    # ---------------------------------------------------------
    initials = (first_name[:1] + last_name[:1]).upper() if first_name or last_name else "HR"

    st.markdown(
        f"""
        <div class="profile-hero">
            <div class="avatar">{initials}</div>
            <div class="hero-name">{full_name}</div>
            <div class="hero-subtitle">
                {role} • {department} • {branch}
            </div>
            <span class="hero-pill">● {status}</span>
            <span class="hero-pill">Employee ID: {employee_id}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------------
    # HR Summary
    # ---------------------------------------------------------
    st.markdown('<div class="section-title">📊 HR Summary</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Leave Balance</div>
                <div class="metric-value">{leave_balance} Days</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Attendance</div>
                <div class="metric-value">{attendance}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Status</div>
                <div class="metric-value">{status}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---------------------------------------------------------
    # Personal Information
    # ---------------------------------------------------------
    st.markdown('<div class="section-title">👤 Personal Information</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">Full Name</div>
                <div class="info-value">{full_name}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">Employee ID</div>
                <div class="info-value">{employee_id}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---------------------------------------------------------
    # Contact
    # ---------------------------------------------------------
    st.markdown('<div class="section-title">📞 Contact Information</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">📧 Email</div>
                <div class="info-value">{email}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">📱 Phone</div>
                <div class="info-value">{phone}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">🌍 Country</div>
                <div class="info-value">{country}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">🗣 Language</div>
                <div class="info-value">{language}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---------------------------------------------------------
    # Professional Information
    # ---------------------------------------------------------
    st.markdown('<div class="section-title">💼 Professional Information</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">🏢 Department</div>
                <div class="info-value">{department}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">📍 Branch</div>
                <div class="info-value">{branch}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">📅 Joining Date</div>
                <div class="info-value">{joining_date}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">🕒 Employment Type</div>
                <div class="info-value">{employment_type}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">🏠 Work Mode</div>
                <div class="info-value">{work_mode}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">👨‍💼 Reporting Manager</div>
                <div class="info-value">{reporting_manager}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---------------------------------------------------------
    # Skills
    # ---------------------------------------------------------
    st.markdown('<div class="section-title">🛠 Skills</div>', unsafe_allow_html=True)

    skills_html = "".join(f'<span class="skill">{skill}</span>' for skill in skills)
    if skills_html:
        st.markdown(skills_html, unsafe_allow_html=True)
    else:
        st.info("No skills available for this employee profile.")

    # ---------------------------------------------------------
    # Emergency Contact
    # ---------------------------------------------------------
    st.markdown('<div class="section-title">🚑 Emergency Contact</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">Name</div>
                <div class="info-value">{emergency_name}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">Relation</div>
                <div class="info-value">{emergency_relation}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">Phone</div>
                <div class="info-value">{emergency_phone}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---------------------------------------------------------
    # Documents
    # ---------------------------------------------------------
    st.markdown('<div class="section-title">📂 Employee Documents</div>', unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3)

    with d1:
        st.markdown(
            """
            <div class="doc-card">
                <div class="doc-icon">🪪</div>
                <strong>Employee ID Card</strong>
                <div class="small-muted">Official identification</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button("View ID Card", use_container_width=True, key="view_id_card")

    with d2:
        st.markdown(
            """
            <div class="doc-card">
                <div class="doc-icon">📄</div>
                <strong>Offer Letter</strong>
                <div class="small-muted">Employment offer document</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button("View Offer Letter", use_container_width=True, key="view_offer_letter")

    with d3:
        st.markdown(
            """
            <div class="doc-card">
                <div class="doc-icon">📜</div>
                <strong>Experience Letter</strong>
                <div class="small-muted">Employment experience document</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button("View Experience Letter", use_container_width=True, key="view_experience_letter")

    # ---------------------------------------------------------
    # Actions
    # ---------------------------------------------------------
    st.markdown('<div class="section-title">⚙️ Profile Actions</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        if st.button("✏️ Edit Profile", use_container_width=True, key="edit_profile"):
            st.info("Profile editing module will be added later.")

    with c2:
        if st.button("📤 Upload Photo", use_container_width=True, key="upload_photo"):
            st.info("Photo upload module will be added later.")

    # ---------------------------------------------------------
    # Security note
    # ---------------------------------------------------------
    st.divider()
    st.caption("🔒 Sensitive authentication information is not displayed on this page.")
