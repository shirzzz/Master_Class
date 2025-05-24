import mysql.connector
from faker import Faker
import random
import insert_tables

fake = Faker()


def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',      # Replace with your MySQL username
        password='',  # Replace with your MySQL password
        database='grouping_db'     # Make sure this DB exists or create it below
    )


# def insert_traits(cursor):
#     traits = ['GPA', 'ADHD', 'BehaviorScore']
#     for trait_name in traits:
#         insert_tables.insert_trait(cursor, trait_name)
#
#
def insert_students_and_traits(cursor):
#     cursor.execute("SELECT trait_id, trait_name FROM Traits")
#     traits = cursor.fetchall()

    for student_id in range(1, 101):
        student_name = fake.name()
        password = "password123"

        insert_tables.insert_student(cursor, student_id, student_name, password)

        # for trait_id, trait_name in traits:
        #     if trait_name == 'GPA':
        #         value = int(random.uniform(11, 100))
        #     elif trait_name == 'ADHD':
        #         value = random.choices([0,1], weights=[0.85, 0.15])[0]
        #     elif trait_name == 'BehaviorScore':
        #         value = random.randint(1, 5)
        #     insert_tables.insert_student_trait_value(cursor, student_id, trait_id, value)


def insert_preferences(cursor):
    for student_id in range(1, 101):
        friends = random.sample([i for i in range(1, 101) if i != student_id], 3)
        for friend_id in friends:
            try:
                insert_tables.insert_student_preference(cursor, student_id, friend_id)
            except:
                pass  # Just in case of duplicates


if __name__ == "__main__":
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # print("Creating traits...")
        # insert_traits(cursor)

        print("Inserting students and their traits...")
        insert_students_and_traits(cursor)

        print("Inserting preferences...")
        insert_preferences(cursor)

        conn.commit()
        cursor.close()
        conn.close()
        print("Mock data created successfully.")

    except mysql.connector.Error as err:
        print(err)
