def get_student_neighbors():
    import mysql.connector

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='grouping_db'
    )
    cursor = conn.cursor()

    # Get the maximum student_id to size the list
    cursor.execute("SELECT MAX(student_id) FROM Students")
    max_id = cursor.fetchone()[0]
    neighbors = [[] for _ in range(max_id)]

    # Query all preferences
    cursor.execute("SELECT student_id, prefers_with FROM StudentPreferences")
    for student_id, prefers_with in cursor.fetchall():
        neighbors[student_id - 1].append(prefers_with)

    cursor.close()
    conn.close()
    return neighbors