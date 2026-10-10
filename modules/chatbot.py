import re
import uuid
from datetime import datetime

import streamlit as st

from chatbot.predictor import predict
from chatbot.database import save_chat, load_chat
from chatbot.openai_api import OpenAIHRAPI


# ---------------------------------------------------------
# Intent groups
# ---------------------------------------------------------

HR_INTENTS = {
    "greeting",
    "leave_balance",
    "apply_leave",
    "attendance",
    "salary",
    "profile",
    "hr",
    "leave_policy",
    "working_hours",
    "office_timing",
    "holiday",
    "company_policy",
    "dress_code",
    "wfh",
    "training",
    "bonus",
    "tax",
    "pf",
    "goodbye",
}


# Sensitive / complex topics should be referred to human HR.
SENSITIVE_TERMS = {
    "harassment",
    "sexual harassment",
    "discrimination",
    "bullying",
    "retaliation",
    "threat",
    "abuse",
    "manager complaint",
    "manager is harassing",
    "unfair treatment",
    "legal complaint",
    "lawsuit",
    "police complaint",
    "salary dispute",
    "wrong salary",
    "termination dispute",
    "disciplinary action",
    "misconduct",
    "confidential complaint",
    "grievance",
}


# Intents where the backend has employee-specific information.
DATA_INTENTS = {
    "leave_balance",
    "attendance",
    "profile",
}


def _safe_employee_context(employee: dict) -> dict:
    """
    Return only the employee fields that are appropriate for the
    HR assistant. Password/authentication fields are intentionally removed.
    """
    allowed_fields = {
        "employee_id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "country",
        "language",
        "branch_name",
        "department_name",
        "role_name",
        "joining_date",
        "leave_balance",
        "attendance",
        "status",
    }

    return {
        key: employee.get(key)
        for key in allowed_fields
        if key in employee
    }


def _is_sensitive_query(question: str) -> bool:
    text = question.lower().strip()
    return any(term in text for term in SENSITIVE_TERMS)


def _rule_based_intent(question: str):
    """
    Fast, deterministic intent routing for common HR questions.
    This prevents a weak/ambiguous classifier from mapping obvious
    questions such as "working hours policy" to an unrelated intent.
    Returns an intent string or None.
    """
    text = question.lower().strip()

    # Greetings / goodbye
    if re.search(r"\b(hi|hello|hey|namaste|good morning|good afternoon|good evening)\b", text):
        return "greeting"

    if re.search(r"\b(bye|goodbye|see you|thank you|thanks)\b", text):
        return "goodbye"

    # Employee-specific data
    if (
        ("leave" in text or "leaves" in text) and
        any(term in text for term in ["how many", "balance", "remaining", "left"])
    ):
        return "leave_balance"

    if any(term in text for term in ["attendance", "absent", "present", "attendance percentage"]):
        return "attendance"

    if any(term in text for term in ["my profile", "my details", "employee details", "my department", "my role"]):
        return "profile"

    # Policy / FAQ questions — these should go to the LLM or RAG,
    # not to the employee-data path.
    policy_patterns = [
        (["working hours", "work hours", "hours of work", "working time"], "working_hours"),
        (["office timing", "office timings", "office time", "when does office open", "when does office close"], "office_timing"),
        (["leave policy", "leave rules", "leave rules"], "leave_policy"),
        (["holiday", "holidays", "holiday list", "holiday calendar"], "holiday"),
        (["wfh", "work from home", "remote work", "work from home policy"], "wfh"),
        (["dress code", "dress policy"], "dress_code"),
        (["company policy", "company policies", "code of conduct"], "company_policy"),
        (["training", "training program", "learning program"], "training"),
        (["bonus", "incentive", "bonus policy"], "bonus"),
        (["salary", "payslip", "pay slip", "salary credit", "payday"], "salary"),
        (["tax", "income tax", "tax deduction"], "tax"),
        (["pf", "provident fund", "epf"], "pf"),
        (["apply leave", "request leave", "take leave", "apply for leave"], "apply_leave"),
    ]

    for keywords, intent in policy_patterns:
        if any(keyword in text for keyword in keywords):
            return intent

    return None


def _create_hr_ticket(employee_id: str, question: str) -> str:
    """
    Creates a local ticket reference for the current project.

    Later this can be connected to the real HR ticket database/email system.
    """
    ticket_id = f"HR-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    st.session_state["last_hr_ticket"] = {
        "ticket_id": ticket_id,
        "employee_id": employee_id,
        "question": question,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "Open",
    }

    return ticket_id


def _build_employee_context(employee: dict, intent: str) -> str:
    """
    Gives the LLM only relevant backend information.
    """
    safe_employee = _safe_employee_context(employee)

    if intent in DATA_INTENTS:
        return (
            "Verified employee data from the HR backend follows. "
            "Use these values when answering employee-specific questions. "
            "Do not invent values.\n\n"
            f"{safe_employee}"
        )

    return (
        "Basic verified employee context follows. "
        "Use it only when relevant and do not expose information unnecessarily.\n\n"
        f"{safe_employee}"
    )


def _build_conversation_context() -> list:
    """
    Send only a small recent window to the model to preserve context
    without growing the request indefinitely.
    """
    history = st.session_state.get("chat_history", [])
    recent = history[-8:]

    context = []

    for chat in recent:
        context.append(
            {
                "role": "user",
                "content": chat["question"],
            }
        )

        context.append(
            {
                "role": "assistant",
                "content": chat["answer"],
            }
        )

    return context


def _handle_local_intent(question: str, intent: str, employee: dict):
    """
    Handles simple deterministic cases locally.
    Returns None when the LLM should answer.
    """

    if intent == "greeting":
        first_name = employee.get("first_name", "there")
        return f"Hello {first_name}! 👋 How can I help you with your HR-related query?"

    if intent == "goodbye":
        return "You're welcome. Have a great day!"

    # Employee-specific values are read from the backend and not generated by AI.
    if intent == "leave_balance":
        balance = employee.get("leave_balance")
        if balance is not None:
            return (
                f"You currently have **{balance} days of leave balance** "
                "available according to the HR records."
            )

    if intent == "attendance":
        attendance = employee.get("attendance")
        if attendance is not None:
            return (
                f"Your recorded attendance is **{attendance}%** "
                "according to the current HR records."
            )

    if intent == "profile":
        return (
            f"You are registered as **{employee.get('first_name', '')} "
            f"{employee.get('last_name', '')}** "
            f"(Employee ID: {employee.get('employee_id', 'N/A')}). "
            f"Department: **{employee.get('department_name', 'N/A')}**. "
            f"Role: **{employee.get('role_name', 'N/A')}**."
        )

    return None


def chatbot_page():

    # ---------------------------------------------------------
    # Employee/session validation
    # ---------------------------------------------------------

    employee = st.session_state.get("employee")

    if not employee:
        st.error("Please log in to use the HR Assistant.")
        return

    employee_id = employee.get("employee_id", "UNKNOWN")

    # ---------------------------------------------------------
    # Page styling
    # ---------------------------------------------------------

    st.markdown(
        """
        <style>
        .chat-header {
            padding: 24px 26px;
            border-radius: 18px;
            background: linear-gradient(135deg, #172554 0%, #1d4ed8 100%);
            color: white;
            margin-bottom: 20px;
        }

        .chat-title {
            font-size: 28px;
            font-weight: 750;
            margin-bottom: 5px;
        }

        .chat-subtitle {
            font-size: 14px;
            opacity: 0.9;
        }

        .support-card {
            padding: 15px 18px;
            border-radius: 14px;
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            margin-bottom: 15px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="chat-header">
            <div class="chat-title">🤖 Smart HR Assistant</div>
            <div class="chat-subtitle">
                Ask questions about HR policies, leave, attendance,
                payroll, workplace procedures and employee support.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        f"Employee: {employee.get('first_name', '')} {employee.get('last_name', '')}"
        f" • ID: {employee_id}"
    )

    # ---------------------------------------------------------
    # Load saved history
    # ---------------------------------------------------------

    if "chat_history" not in st.session_state:

        try:
            history = load_chat(employee_id)
        except Exception:
            history = []

        st.session_state.chat_history = []

        for row in history:
            # sqlite3.Row is dict-like but does not support .get()
            st.session_state.chat_history.append(
                {
                    "question": row["question"] if "question" in row.keys() else "",
                    "answer": row["answer"] if "answer" in row.keys() else "",
                }
            )

    # ---------------------------------------------------------
    # Show recent messages
    # ---------------------------------------------------------

    for chat in st.session_state.chat_history:

        with st.chat_message("user"):
            st.write(chat["question"])

        with st.chat_message("assistant"):
            st.write(chat["answer"])

    # ---------------------------------------------------------
    # User question
    # ---------------------------------------------------------

    question = st.chat_input("Ask your HR question...")

    if question:

        question = question.strip()

        if not question:
            st.warning("Please enter a question.")
            st.stop()

        # ---------------------------------------------
        # 1. Determine intent
        # ---------------------------------------------
        # Use deterministic rules first for obvious HR queries.
        # Fall back to the existing NLP predictor only when the
        # rule-based router cannot confidently classify the query.
        intent = _rule_based_intent(question)

        if intent is None:
            try:
                result = predict(question)
                intent = result.get("intent", "hr")
            except Exception:
                intent = "hr"

        # ---------------------------------------------
        # 2. Sensitive/complex escalation
        # ---------------------------------------------
        if _is_sensitive_query(question):

            ticket_id = _create_hr_ticket(employee_id, question)

            answer = (
                "I understand your concern. This matter may require "
                "confidential human HR attention, so I have created an "
                "HR support ticket for human review.\n\n"
                f"**HR Ticket:** `{ticket_id}`\n"
                f"**Status:** Open\n\n"
                "A human HR representative can review the matter "
                "according to your organization's HR process."
            )

        else:

            # ---------------------------------------------
            # 3. Handle deterministic employee data cases
            # ---------------------------------------------
            local_answer = _handle_local_intent(
                question,
                intent,
                employee,
            )

            if local_answer:
                answer = local_answer

            else:

                # ---------------------------------------------
                # 4. Send normal HR question to ChatGPT
                # ---------------------------------------------
                try:
                    hr_ai = OpenAIHRAPI()

                    employee_context = _build_employee_context(
                        employee,
                        intent,
                    )

                    conversation = _build_conversation_context()

                    answer = hr_ai.ask(
                        question=question,
                        intent=intent,
                        employee_context=employee_context,
                        conversation=conversation,
                    )

                    if not answer:
                        answer = (
                            "I could not process that request right now. "
                            "Please try again or contact HR."
                        )

                except Exception as exc:
                    # Keep the actual exception out of the UI.
                    print(f"HR Assistant API error: {exc}")

                    answer = (
                        "The AI HR Assistant is temporarily unavailable. "
                        "Please try again in a moment."
                    )

        # ---------------------------------------------
        # 5. Save conversation
        # ---------------------------------------------
        try:
            save_chat(
                employee_id,
                question,
                answer,
                intent,
            )
        except Exception as exc:
            print(f"Chat history save error: {exc}")

        # ---------------------------------------------
        # 6. Update current session
        # ---------------------------------------------
        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": answer,
            }
        )

        st.rerun()

    # ---------------------------------------------------------
    # Bottom actions
    # ---------------------------------------------------------

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        if st.button(
            "🗑 Clear Current Session Chat",
            use_container_width=True,
        ):
            st.session_state.chat_history = []
            st.session_state.pop("last_hr_ticket", None)
            st.rerun()

    with c2:
        if st.button(
            "👤 Request Human HR Support",
            use_container_width=True,
        ):
            ticket_id = _create_hr_ticket(
                employee_id,
                "Employee requested human HR support.",
            )

            st.success(
                f"HR support request created: {ticket_id}"
            )
