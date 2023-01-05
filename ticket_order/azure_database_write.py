import mysql.connector
from mysql.connector import errorcode

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

  # Drop previous table of same name if one exists
  cursor.execute("DROP TABLE IF EXISTS ticket_order;")
  print("Finished dropping table (if existed).")

  # Create table
  cursor.execute("CREATE TABLE ticket_order (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT , travel_date VARCHAR(20), \
    travel_time VARCHAR(20), boarding VARCHAR(20), get_off VARCHAR(20), seat INT, name VARCHAR(20), ticket VARCHAR(20), \
    price VARCHAR(20), coupon VARCHAR(20), ticket_num VARCHAR(20), order_num VARCHAR(20));")
  print("Finished creating table.")

  # Insert some data into table
#   cursor.execute("INSERT INTO ticket_order VALUES (0, '2023/01/19(四)', '16:15', '台北轉運站(經新營)', '高雄九如站', '12', '駱忠湧', '專案票', '630', '0', 'IP046O00008060', '2314Y7VEW2');")
#   cursor.execute("INSERT INTO ticket_order VALUES (0, '2023/01/18(四)', '16:15', '台北轉運站(經新營)', '高雄九如站', '12', '駱忠湧', '專案票', '630', '0', 'IP046O00008060', '2314Y7VEW2');")

  # Cleanup
  conn.commit()
  cursor.close()
  conn.close()
  print("Done.")