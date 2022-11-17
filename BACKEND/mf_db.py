
import pymysql
from datetime import datetime

class MFDataDb :
    def __init__(self):
        self.host = 'stock-info-db.c6lwd3w67mnt.us-west-2.rds.amazonaws.com'
        self.username ='juhi'
        self.password='JgE2EJip2qhWywax2Gw8'
        self.database='StockDB'
        self.conn = None
        self.conn_cursor = None

        return

    def connect(self):
        self.conn = pymysql.connect(host=self.host,
                             user=self.username,
                             password=self.password,
                             db=self.database,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        self.conn_cursor = self.conn.cursor()

        return

    def is_connected(self):
        return (not(self.conn == None))

    def close(self):
        self.conn.close()
        self.conn = None
        self.conn.cursor = None
        return

    def exec_read_query(self,query_str):
        self.conn_cursor.execute(query_str)
        return self.conn_cursor
        
    def exec_write_query(self,query_str):
        try:
            self.conn_cursor.execute(query_str)
            self.conn.commit()
        except:
            self.conn.rollback()
        return
 
        
if __name__ =="__main__":
    dbconn = MFDataDb() 
    dbconn.connect()

    c = dbconn.exec_read_query('SELECT * FROM WEEKLYPRICE where ticker="ABB.BSE" limit 10;')
    # while True:
    #     row = c.fetchone()
    #     if (row == None):
    #         break
    #     print(row)
    #     print(row['tradedate'].isoformat())
    rows = c.fetchall()
    for r in rows:
        print(r)



