import mysql.connector
from mysql.connector import errorcode

def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',      # Replace with your MySQL username
        password='',  # Replace with your MySQL password
        database='grouping_db'     # Make sure this DB exists or create it below
    )

def create_tables(cursor):
    TABLES = {}

    TABLES["Users"] = """
        CREATE TABLE IF NOT EXISTS Users (
            user_id INT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        );
    """

    TABLES["Students"] = """
        CREATE TABLE IF NOT EXISTS Students (
            student_id INT PRIMARY KEY,
            student_name VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            FULLTEXT student_name_index (student_name)
        );
    """

    # TABLES["Traits"] = """
    #     CREATE TABLE IF NOT EXISTS Traits (
    #         trait_id INT AUTO_INCREMENT PRIMARY KEY,
    #         trait_name VARCHAR(255) NOT NULL,
    #         FULLTEXT trait_name_index (trait_name)
    #     );
    # """
    #
    # TABLES["StudentTraitValues"] = """
    #     CREATE TABLE IF NOT EXISTS StudentTraitValues (
    #         student_id INT NOT NULL,
    #         trait_id INT NOT NULL,
    #         value INT NOT NULL,
    #         PRIMARY KEY (student_id, trait_id),
    #         FOREIGN KEY (student_id) REFERENCES Students(student_id),
    #         FOREIGN KEY (trait_id) REFERENCES Traits(trait_id)
    #     );
    # """

    TABLES["StudentPreferences"] = """
        CREATE TABLE IF NOT EXISTS StudentPreferences (
            student_id INT NOT NULL,
            prefers_with INT NOT NULL,
            PRIMARY KEY (student_id, prefers_with),
            FOREIGN KEY (student_id) REFERENCES Students(student_id),
            FOREIGN KEY (prefers_with) REFERENCES Students(student_id)
        );
    """

    # TABLES["GroupingSessions"] = """
    #     CREATE TABLE IF NOT EXISTS GroupingSessions (
    #         session_id INT AUTO_INCREMENT PRIMARY KEY,
    #         advisor_id INT NOT NULL,
    #         session_name VARCHAR(255) NOT NULL,
    #         date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    #         FOREIGN KEY (advisor_id) REFERENCES Users(user_id)
    #     );
    # """
    #
    # TABLES["TraitWeights"] = """
    #     CREATE TABLE IF NOT EXISTS TraitWeights (
    #         session_id INT NOT NULL,
    #         trait_id INT NOT NULL,
    #         weight INT CHECK (weight >= 1 and weight <= 10),
    #         PRIMARY KEY (session_id, trait_id),
    #         FOREIGN KEY (session_id) REFERENCES GroupingSessions(session_id),
    #         FOREIGN KEY (trait_id) REFERENCES Traits(trait_id)
    #     );
    # """
    #
    # TABLES["Classes"] = """
    #     CREATE TABLE IF NOT EXISTS Classes (
    #         group_id INT AUTO_INCREMENT PRIMARY KEY,
    #         session_id INT NOT NULL,
    #         class_name VARCHAR(100),
    #         FOREIGN KEY (session_id) REFERENCES GroupingSessions(session_id)
    #     );
    # """
    #
    # TABLES["GroupMembers"] = """
    #     CREATE TABLE IF NOT EXISTS GroupMembers (
    #         group_id INT NOT NULL,
    #         student_id INT NOT NULL,
    #         PRIMARY KEY (group_id, student_id),
    #         FOREIGN KEY (group_id) REFERENCES Classes(group_id),
    #         FOREIGN KEY (student_id) REFERENCES Students(student_id)
    #     );
    # """

    for name, ddl in TABLES.items():
        try:
            cursor.execute(ddl)
            print(f"Created table `{name}`")
        except mysql.connector.Error as err:
            print(f"Failed creating table `{name}`: {err}")

if __name__ == "__main__":
    try:
        conn = create_connection()
        cursor = conn.cursor()
        create_tables(cursor)
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist. Please create the database `grouping_db` first.")
        else:
            print(err)
