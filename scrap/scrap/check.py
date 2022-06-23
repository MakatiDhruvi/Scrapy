import psycopg2

hostname = 'localhost'
username = 'postgres'
password = 'Dhruvi@2001' 
database = 'quotes'

def queryQuotes( conn ) :
    cur = conn.cursor()
    cur.execute("select count(*) from public.quotes where title = %s",(adapter['title'][0][1:-1]))
    rows = cur.fetchall()

    for row in rows :
        print (row[1])

conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
queryQuotes( conn )
conn.close()
