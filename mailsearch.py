import sqlite3

#connecting to databse
conn=sqlite3.connect('mymail.db')
cur=conn.cursor()
cur.execute('''SELECT * FROM MAIL''')
indicator=False

#Performing search
findtxt=input('Search For: ')
while True:
    findtxtin=input('Search In: ')
    if findtxtin=='quit':
        quit()
    for i in cur.description:
        if i[0]==findtxtin:
            indicator=True
            break
        else:
            continue
    if indicator==False:
        print('Incorrect Column name:')
        continue
    cur.execute('''SELECT %s FROM MAIL'''%(findtxtin))
    rows=cur.fetchall()
    prind=False
    for row in rows:
        if findtxt.lower() in str(row[0]).lower():
            print(str(row[0]).strip())
            prind=True
    if prind==False:
        print('No match')
