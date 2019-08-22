# worker.py
from database.connection import connection
from worker_functions import retrieve_and_insert_readings_for_all_addresses


def main():

<<<<<<< HEAD
    # remote version
    db_url = os.environ.get('DATABASE_URL')

    # local version
    if db_url is None:
        proc = subprocess.Popen('heroku config:get DATABASE_URL -a rqa', stdout=subprocess.PIPE, shell=True)
        db_url = proc.stdout.read().decode('utf-8').strip() + '?sslmode=require'

    conn = psycopg2.connect(db_url)
    conn.autocommit = True
    cur = conn.cursor()
=======
    cur, conn = connection.open_database_connection()
>>>>>>> develop

    retrieve_and_insert_readings_for_all_addresses(cur)

    # conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
