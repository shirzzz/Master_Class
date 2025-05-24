import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',      # Replace with your MySQL username
        password='',  # Replace with your MySQL password
        database='grouping_db'     # Make sure this DB exists or create it below
    )

def insert_user(cursor, user_id, username, password):
    cursor.execute("""
        INSERT INTO Users (user_id, username, password)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            username = VALUES(username),
            password = VALUES(password)
    """, (user_id, username, password))

def insert_student(cursor, student_id, student_name, password):
    cursor.execute("""
        INSERT INTO Students (student_id, student_name, password)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            student_name = VALUES(student_name),
            password = VALUES(password);
    """, (student_id, student_name, password))

# def insert_trait(cursor, trait_name):
#     cursor.execute("""
#         INSERT INTO Traits (trait_name)
#         VALUES (%s)
#         ON DUPLICATE KEY UPDATE trait_name = VALUES(trait_name);
#     """, (trait_name,))
#
# def insert_student_trait_value(cursor, student_id, trait_id, value):
#     cursor.execute("""
#         INSERT INTO StudentTraitValues (student_id, trait_id, value)
#         VALUES (%s, %s, %s)
#         ON DUPLICATE KEY UPDATE value = VALUES(value);
#     """, (student_id, trait_id, value))

def insert_student_preference(cursor, student_id, prefers_with_id):
    cursor.execute("""
        INSERT INTO StudentPreferences (student_id, prefers_with)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE prefers_with = VALUES(prefers_with);
    """, (student_id, prefers_with_id))

# def insert_grouping_session(cursor, advisor_id, session_name):
#     cursor.execute("""
#         INSERT INTO GroupingSessions (advisor_id, session_name)
#         VALUES (%s, %s)
#         ON DUPLICATE KEY UPDATE advisor_id = VALUES(advisor_id);
#     """, (advisor_id, session_name))
#     return cursor.lastrowid  # return session_id
#
# def insert_trait_weight(cursor, session_id, trait_id, weight):
#     cursor.execute("""
#         INSERT INTO TraitWeights (session_id, trait_id, weight)
#         VALUES (%s, %s, %s)
#         ON DUPLICATE KEY UPDATE weight = VALUES(weight);
#     """, (session_id, trait_id, weight))
#
# def insert_class(cursor, session_id, name):
#     cursor.execute("""
#         INSERT INTO Classes (session_id, class_name)
#         VALUES (%s, %s)
#         ON DUPLICATE KEY UPDATE session_id = VALUES(session_id), class_name = VALUES(class_name);
#     """, (session_id, name))
#     return cursor.lastrowid  # return group_id
#
# def insert_group_member(cursor, group_id, student_id):
#     cursor.execute("""
#         INSERT INTO GroupMembers (group_id, student_id)
#         VALUES (%s, %s)
#         ON DUPLICATE KEY UPDATE group_id = VALUES(group_id);
#     """, (group_id, student_id))

# Example usage
def main():
    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Example: insert one advisor
        insert_user(cursor, 1, "dana@school.edu", "DanaPass123")

        # Example: insert a trait
#        insert_trait(cursor, "Behavior")

        # You can keep calling other insert functions here as needed
        conn.commit()
        print("Insertions completed successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
   main()
