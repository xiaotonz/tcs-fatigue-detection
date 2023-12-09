import mysql.connector
from config import read_config
from constants import UNKNOWN_EMPLOYEE, UNKNOWN_SHIFT

def initialize_database(config):
    host = config['db']['host']
    user = config['db']['user']
    password = config['db']['password'].strip('"')
    database = config['db']['database']
    db_connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    db_cursor = db_connection.cursor(dictionary=True)
    return db_connection, db_cursor


def insert_or_update_employee(db_cursor, emp_id, emp_name, emp_position, emp_shift):
    query = """
    INSERT INTO EMPLOYEE (emp_id, emp_name, emp_position, emp_shift)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE emp_name=%s, emp_position=%s, emp_shift=%s
    """
    values = (emp_id, emp_name, emp_position, emp_shift, emp_name, emp_position, emp_shift)
    db_cursor.execute(query, values)

def insert_or_update_fatigue_history_index(db_connection, db_cursor, timestamp, emp_id, fatigue_index):
    # Convert the fatigue status to an integer, if it's not already
    # fatigue_status = int(fatigue_status)

    # Query to check if the employee exists in the EMPLOYEE table
    employee_query = "SELECT * FROM EMPLOYEE WHERE emp_id = %s"
    db_cursor.execute(employee_query, (emp_id,))
    employee = db_cursor.fetchone()

    # If the employee does not exist, insert a new record
    if employee is None:
        print(f"Employee with ID {emp_id} does not exist, inserting...")
        insert_or_update_employee(db_cursor, emp_id, UNKNOWN_EMPLOYEE, UNKNOWN_EMPLOYEE, UNKNOWN_SHIFT)

    # Check if a record with the same timestamp and emp_id exists in FATIGUE_HISTORY_INDEX
    fatigue_query = "SELECT * FROM fatigue_history_index WHERE created_at = %s AND emp_id = %s"
    db_cursor.execute(fatigue_query, (timestamp, emp_id))
    fatigue_record = db_cursor.fetchone()

    if not fatigue_record:
        insert_query = "INSERT INTO fatigue_history_index (created_at, emp_id, fatigue_index) VALUES (%s, %s, %s)"
        db_cursor.execute(insert_query, (timestamp, emp_id, fatigue_index))
        # If the record exists, update the fatigue_status
        # update_query = "UPDATE FATIGUE_HISTORY SET fatigue_status = %s WHERE timestamp = %s AND emp_id = %s"
        # db_cursor.execute(update_query, (fatigue_status, timestamp, emp_id))
    else:
        update_query = "UPDATE fatigue_history_index SET fatigue_index = %s WHERE timestamp = %s AND emp_id = %s"
        db_cursor.execute(update_query, (fatigue_index, timestamp, emp_id))


    # Commit the transaction
    db_connection.commit()


def insert_or_update_fatigue_history(db_connection, db_cursor, timestamp, emp_id):
    # Convert the fatigue status to an integer, if it's not already
    # fatigue_status = int(fatigue_status)

    # Query to check if the employee exists in the EMPLOYEE table
    employee_query = "SELECT * FROM EMPLOYEE WHERE emp_id = %s"
    db_cursor.execute(employee_query, (emp_id,))
    employee = db_cursor.fetchone()

    # If the employee does not exist, insert a new record
    if employee is None:
        print(f"Employee with ID {emp_id} does not exist, inserting...")
        insert_or_update_employee(db_cursor, emp_id, UNKNOWN_EMPLOYEE, UNKNOWN_EMPLOYEE, UNKNOWN_SHIFT)

    # Check if a record with the same timestamp and emp_id exists in FATIGUE_HISTORY
    fatigue_query = "SELECT * FROM FATIGUE_HISTORY WHERE created_at = %s AND emp_id = %s"
    db_cursor.execute(fatigue_query, (timestamp, emp_id))
    fatigue_record = db_cursor.fetchone()

    if not fatigue_record:
        insert_query = "INSERT INTO FATIGUE_HISTORY (created_at, emp_id) VALUES (%s, %s)"
        db_cursor.execute(insert_query, (timestamp, emp_id))
        # If the record exists, update the fatigue_status
        # update_query = "UPDATE FATIGUE_HISTORY SET fatigue_status = %s WHERE timestamp = %s AND emp_id = %s"
        # db_cursor.execute(update_query, (fatigue_status, timestamp, emp_id))
    # else:
    # If the record does not exist, insert a new one

    # Commit the transaction
    db_connection.commit()

def main():
    config = read_config('config.ini')
    db_connection, db_cursor = initialize_database(config)

if __name__ == "__main__":
    main()
