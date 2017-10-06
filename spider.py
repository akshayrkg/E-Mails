import urllib.error,urllib.request,urllib.parse
import sqlite3
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url="http://mbox.dr-chuck.net/sakai.devel/"
start=0
conn=sqlite3.connect('mymail.db')
cur=conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS MAIL(
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,email_id INTEGER, subject TEXT, header TEXT,
 body TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS eid(
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,email TEXT UNIQUE)''')

howmany=input('How many emails: ')
while True:
    try:
        howmany=int(howmany)
        break
    except:
        if howmany != 'qui':
            print('Integer only'+'\n'+'To quit press qui')
            continue
        else:
            quit()
i=0
while i<howmany:
    cur.execute('''SELECT max(id) FROM MAIL''')
    row1=cur.fetchone()
    if row1[0] == None:
        start=0
    else:
        start=row1[0]
    start=start+1
    baseurl=url+str(start)+'/'+str(start+1)
    try:
        urlhand=urllib.request.urlopen(baseurl,None,5,context=ctx)
        data=urlhand.read().decode()
        if urlhand.getcode() != 200 :
            print("Error code=",document.getcode(), url)
            break
    except KeyboardInterrupt:
        print('Program interrupted by user...')
        break
    except Exception as e:
        print('Error Desc',e)
        continue
    email=re.findall('From: .*<(\S*@\S*)>',data)
    print(email)

    cur.execute('''
    INSERT OR IGNORE INTO eid (email) VALUES (?)''',(email[0],))

    subject=re.findall('Subject: (.*)\n',data)
    bodypos=data.find('\n\n')
    header=data[:bodypos]
    body=data[bodypos+2:]
    cur.execute('''SELECT id FROM eid WHERE email=?''',(email[0],))
    row=cur.fetchone()

    cur.execute('''
    INSERT OR IGNORE INTO MAIL (email_id,subject,header,body) VALUES
    (?,?,?,?)''',(row[0],subject[0],header,body))
    conn.commit()

    i=i+1

conn.commit()
cur.close()
