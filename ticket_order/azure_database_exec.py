import mysql.connector
from mysql.connector import errorcode


def exec_database(exec="SELECT * FROM ticket_order;"):
    # Obtain connection string information from the portal

    config = {
    'host':'heroku.mysql.database.azure.com',
    'user':'daniel',
    'password':'5627Abcd',
    'database':'bus',
    'client_flags': [mysql.connector.ClientFlag.SSL],
    'ssl_ca': '/Users/daniel/Downloads/DigiCertGlobalRootG2.crt.pem'
    }

    # Construct connection string

    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()

        # Read data
        cursor.execute(exec)
        rows = cursor.fetchall()
        # print("Read",cursor.rowcount,"row(s) of data.")

        # Print all rows
        for row in rows:
            print(row)

        # Cleanup
        conn.commit()
        cursor.close()
        conn.close()
        print("Done.")

    return rows

if __name__ == '__main__':
    search_ticket()