import mysql.connector

# --- Configuration ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'grouping_db'
}

# --- Connection Helper ---
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# --- 1. User Login Lookup ---
def login_lookup_staff(username):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM Users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

# --- 2. Student Login Lookup ---
def login_lookup_students(student_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM Students WHERE student_id = %s"
    cursor.execute(query, (student_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

# --- 3. Friends by User ---
def get_friends(student_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT s2.student_id, s2.name AS friend_name
        FROM StudentPreferences sp
        JOIN Students s2 ON sp.prefers_with = s2.student_id
        WHERE sp.student_id = %s
    """
    cursor.execute(query, (student_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# --- 4. Full Text Students + Traits ---
def get_students_with_traits(search_term):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
            SELECT s.student_id, \
                   s.name AS student_name,
                   t.trait_id, \
                   t.trait_name,
                   stv.value
            FROM Students s
                     JOIN StudentTraitValues stv ON s.student_id = stv.student_id
                     JOIN Traits t ON stv.trait_id = t.trait_id
            WHERE MATCH (s.name) AGAINST (%s IN NATURAL LANGUAGE MODE)
               OR MATCH (t.trait_name) AGAINST (%s IN NATURAL LANGUAGE MODE) \
            """
    cursor.execute(query, (search_term, search_term))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# --- 4. Full Text Students + Traits ---
def get_students(student_name, current_student_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
            SELECT s.student_id, s.student_name
            FROM Students s
            WHERE s.student_name LIKE %s
            AND s.student_id NOT IN (SELECT prefers_with FROM StudentPreferences WHERE student_id = %s)
            """
    cursor.execute(query, (f"{student_name}%", current_student_id))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# --- 5. Query Trait Weights for a Session ---
def get_trait_weights(session_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT tw.session_id, t.trait_name, tw.weight
        FROM TraitWeights tw
        JOIN Traits t ON tw.trait_id = t.trait_id
        WHERE tw.session_id = %s
    """
    cursor.execute(query, (session_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# --- Example Usage ---
if __name__ == "__main__":
    # Login lookup
    print("Login lookup:", login_lookup_students(student_id=1))

    # Get friends
    print("Friends:", get_friends(student_id=1))

    # Students and traits
    print("Students with traits:", get_students_with_traits())

    # Clear friends
    # clear_all_friends()
    # print("Cleared all friends.")

    # Trait weights
    print("Trait weights:", get_trait_weights(session_id=1))
