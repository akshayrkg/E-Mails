from textblob import TextBlob
import sqlite3
conn=sqlite3.connect('mymail.db')
cur=conn.cursor()
cur.execute('''SELECT id,body FROM MAIL''')
rows=cur.fetchall()
for row in rows:
    senti=TextBlob(row[1])
    rating=senti.sentiment.polarity
    if rating >0:
        print(row[0],rating,'positive')
    elif rating <0:
        print(row[0],rating,'negative')
    else:
        print(row[0],rating,'neutral')