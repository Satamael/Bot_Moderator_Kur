import datetime
import os
import sqlite3
def sqlite_connect():
    conn = sqlite3.connect("database.db", check_same_thread=False)
    conn.execute("pragma journal_mode=wal;")
    return conn

def init_sqlite():
    if os.path.isfile('database.db'):
        conn = sqlite_connect()
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS muteusers (id integer primary key, user_id integer, user_name text, date_end datetime, cause text)''')
        c.execute('''CREATE TABLE IF NOT EXISTS banusers (  id integer primary key, user_id integer, user_name text, date_ban datetime, status bool, count int, cause text)''')
        conn.commit()
        conn.close()
    return

def getUser(user_id, database):
    conn = sqlite_connect()
    c = conn.cursor()
    if database == 'muteusers':
        c.execute('SELECT user_id FROM muteusers WHERE user_id = :user', {'user': user_id})
    else:
        c.execute('SELECT user_id FROM banusers WHERE user_id = :user', {'user': user_id})
    return list(c.fetchall())

def getCount(user_id):
    conn = sqlite_connect()
    c = conn.cursor()
    c.execute('SELECT count FROM banusers WHERE user_id = :user', {'user': user_id})
    count = c.fetchone()
    return int(count[0])

def insertToMute(user_id, user_name, date, cause):
    conn = sqlite_connect()
    c = conn.cursor()
    rows = getUser(user_id, 'muteusers')
    if len(rows) > 0 and map(lambda s: s.contains(user_id), rows):
        c.execute('UPDATE muteusers SET date_end = ?, cause = ? WHERE user_id = ?',
                  (date, cause, user_id))
    else:
        c.execute('INSERT INTO muteusers (user_id, user_name, date_end, cause) VALUES(?, ?, ?, ?)',
              (user_id, user_name, date, cause))
    conn.commit()
    conn.close()
    return

def insertToBan(user_id, user_name, date_ban, status, cause):
    conn = sqlite_connect()
    c = conn.cursor()
    rows = getUser(user_id, 'banusers')
    if len(rows) > 0 and map(lambda s: s.contains(user_id), rows):
        if status == False:
            c.execute('UPDATE banusers SET status = ? WHERE user_id = ?',
                      (status, user_id))
        else:
            count = getCount(user_id) + 1
            c.execute('UPDATE banusers SET date_ban = ?, status = ?, count = ?, cause = ? WHERE user_id = ?',
                      (date_ban, status, count, cause, user_id))
    else:
        c.execute('INSERT INTO banusers (user_id, user_name, date_ban, status, count, cause) VALUES(?, ?, ?, ?, ?, ?)',
              (user_id, user_name, date_ban, status, 1, cause))
    conn.commit()
    conn.close()
    return


def select_mute_user():
    conn = sqlite_connect()
    c = conn.cursor()
    c.execute(f"SELECT user_id, user_name, cause FROM muteusers where date_end >= DATE('now')")
    rows = c.fetchall()
    list = []
    for i in rows:
        list.append(str(i[0]) + ' '+str(i[1])+' '+str(i[2]))
    return list

def select_ban_user():
    conn = sqlite_connect()
    c = conn.cursor()
    c.execute('SELECT user_name, cause, count FROM banusers WHERE status = True')
    rows = c.fetchall()
    list = []
    for i in rows:
        list.append(str(i[0]) + ' '+str(i[1])+' '+str(i[2]))
    return list