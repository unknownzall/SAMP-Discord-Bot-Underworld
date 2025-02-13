import mysql.connector
import json, random
import string

try:
  with open('mysql.json', 'r') as file:
    config = json.load(file)
except FileNotFoundError:
  config = {}
  
db_host = config['host']
db_user = config['username']
db_pw = config['password']
db_name = config['database']

def check_mysql_connection():
    try:
        # Membuat koneksi ke database MySQL
        connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pw,
        database=db_name
        )
        return True

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False  # Koneksi gagal
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            
def reset_password(discord_id, new_password):
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pw,
        database=db_name
    )

    try:
        cursor = connection.cursor()

        # Mengambil PIN lama dari basis data
        old_pin_query = "SELECT `pin` FROM `ucp` WHERE `DiscordID` = %s"
        old_pin_data = (discord_id,)
        cursor.execute(old_pin_query, old_pin_data)
        old_pin_result = cursor.fetchone()
        old_pin = old_pin_result[0] if old_pin_result else None

        # Menghasilkan PIN acak baru
        new_pin = generate_pin()

        # Menyimpan PIN baru ke dalam basis data
        pin_query = "UPDATE `ucp` SET `pin` = %d WHERE `DiscordID` = %s"
        pin_data = (new_pin, discord_id)
        cursor.execute(pin_query, pin_data)
        
        password_query = "UPDATE `ucp` SET `password` = %s WHERE `DiscordID` = %s"
        password_data = (new_password, discord_id)
        cursor.execute(password_query, password_data)
        
        connection.commit()
        return old_pin, new_pin
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def generate_pin():
    return ''.join(random.choices('0123456789', k=5))

def vouchercode(code, viptype, viptime, gold):
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pw,
        database=db_name
    )

    try:
        cursor = connection.cursor()
        query = "INSERT INTO vouchers (code, vip, vip_time, gold) VALUES (%d, %d, %d, %d)"
        data = (code, viptype, viptime, gold,)
        cursor.execute(query, data)
        connection.commit()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def register_user(ucp_name, verifycode, discord_id, gmail, phone):
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pw,
        database=db_name
    )

    try:
        cursor = connection.cursor()
        query = "INSERT INTO playerucp (UCP, code, DiscordID, email, nohp) VALUES (%s, %s, %s, %s, %s)"
        data = (ucp_name, verifycode, discord_id, gmail, phone)
        cursor.execute(query, data)
        connection.commit()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def characterstory(namachar):
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pw,
        database=db_name
    )

    try:
        cursor = connection.cursor()
        query = "UPDATE `characters` SET `Story` = 1 WHERE `Character` = %s"
        jiramat = (namachar,)
        cursor.execute(query, jiramat)
        connection.commit()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def check_id(user_id):
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pw,
        database=db_name
    )

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT UCP FROM playerucp WHERE DiscordID = %s"
        data = (user_id,)
        cursor.execute(query, data)
        result = cursor.fetchone()

        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            
def ucp_check(ucp):
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pw,
        database=db_name
    )

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT UCP FROM playerucp WHERE UCP = %s"
        data = (ucp,)
        cursor.execute(query, data)
        result = cursor.fetchone()

        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
  
def get_user_info(user_id):
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pw,
        database=db_name
    )

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT DiscordID, UCP, code FROM playerucp WHERE DiscordID = %s"
        data = (user_id,)

        cursor.execute(query, data)
        result = cursor.fetchone()

        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()