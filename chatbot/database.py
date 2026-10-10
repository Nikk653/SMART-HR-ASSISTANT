from db.database import get_connection


def save_chat(employee_id, question, answer, intent):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_history
        (
            employee_id,
            question,
            answer,
            intent
        )
        VALUES(?,?,?,?)
        """,
        (
            employee_id,
            question,
            answer,
            intent
        )
    )

    conn.commit()

    conn.close()


def load_chat(employee_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            question,
            answer
        FROM chat_history

        WHERE employee_id=?

        ORDER BY id
        """,
        (employee_id,)
    )

    data = cursor.fetchall()

    conn.close()

    return data