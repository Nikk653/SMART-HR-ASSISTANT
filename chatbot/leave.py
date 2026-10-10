from db.database import get_connection


def apply_leave(employee_id, leave_date, reason):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO leave_requests
        (
            employee_id,
            leave_date,
            reason
        )
        VALUES(?,?,?)
        """,
        (
            employee_id,
            leave_date,
            reason
        )
    )

    conn.commit()

    conn.close()

    return True