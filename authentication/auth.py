from db.database import get_connection


def login_user(employee_id, password):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT

        e.*,

        b.branch_name,

        d.department_name,

        r.role_name

    FROM employees e

    LEFT JOIN branches b
    ON e.branch_id = b.branch_id

    LEFT JOIN departments d
    ON e.department_id = d.department_id

    LEFT JOIN roles r
    ON e.role_id = r.role_id

    WHERE

    e.employee_id = ?

    AND

    e.password = ?

    """

    cursor.execute(
        query,
        (
            employee_id,
            password
        )
    )

    user = cursor.fetchone()

    conn.close()

    return user