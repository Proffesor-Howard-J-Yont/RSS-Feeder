import sqlite3

conn = sqlite3.connect('info.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS pod_list (
          name text,
          description text,
          image blob,
          amt_clicked integer,
          feed text,
          auto_check integer,
          secret_key text,
          last_checked_number integer)''')

def add_podcast(name, description, image, feed, auto_check, secret_key, last_checked_number):
    # Check to make sure it's not already in the database
    c.execute("SELECT * FROM pod_list WHERE secret_key = ?", (secret_key,))
    if c.fetchone() is not None:
        print("Podcast already exists in the database.")
        return

    c.execute("INSERT INTO pod_list (name, description, image, amt_clicked, feed, auto_check, secret_key, last_checked_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (name, description, image, 0, feed, auto_check, secret_key, last_checked_number))
    # insert picture into database as blob
    c.execute("UPDATE pod_list SET image = ? WHERE secret_key = ?", (sqlite3.Binary(image), secret_key))
    conn.commit()

def get_suggested_podcasts():
    c.execute("SELECT name, description, image, feed, secret_key FROM pod_list ORDER BY amt_clicked DESC LIMIT 5")
    return c.fetchall()

def get_recent_podcasts():
    c.execute("SELECT name, description, image, feed, secret_key FROM pod_list ORDER BY last_checked_number DESC LIMIT 5")
    return c.fetchall()

def increment_click_count(secret_key):
    c.execute("UPDATE pod_list SET amt_clicked = amt_clicked + 1 WHERE secret_key = ?", (secret_key,))
    conn.commit()
    c.execute("SELECT MAX([last_checked_number]) FROM pod_list")
    max_value = c.fetchone()[0]
    c.execute("UPDATE pod_list SET last_checked_number = ? WHERE secret_key = ?", (max_value + 1, secret_key))
    conn.commit()
def grab_podcast(secret_key):
    c.execute("SELECT * FROM pod_list WHERE secret_key = ?", (secret_key,))
    grabbed = c.fetchone()
    if grabbed is None:
        print("Podcast not found in the database.")
        return None
    return grabbed

def get_other_podcasts(): # Get all podcasts except the top 5 suggested
    c.execute("SELECT name, description, image, feed, secret_key FROM pod_list WHERE secret_key NOT IN (SELECT secret_key FROM pod_list ORDER BY amt_clicked DESC LIMIT 5)")
    return c.fetchall()