# worker.py
from database.connection import connection
from worker_functions import retrieve_and_insert_readings_for_all_addresses

def main():

    cur, conn = connection.open_database_connection()

    retrieve_and_insert_readings_for_all_addresses(cur)

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
