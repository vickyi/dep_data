#!/usr/bin/python
#coding=utf-8
import sys
import MySQLdb
import env_config as env

reload(sys)
sys.setdefaultencoding('utf8')

class mysql_crud():
    
    def __init__(self):
    #         self.server = env.local
        self.server = env.server
        self.host = self.server['host']
        self.user = self.server['user']
        self.pwd = self.server['pwd']
        self.db = self.server['db']
        self.charset = self.server['charset']
        
    def mysqlConnect(self):
        """
        #Connection()函数的参数依次为
        #     host(string, host to connect);
        #     user(string, user to connect as);
        #     passwd(string, password to use);
        #     db(string, database to use)
        """
        try:
            return MySQLdb.connect(host=self.host, user=self.user, passwd=self.pwd, db=self.db, charset=self.charset)
        except Exception,e:
            print 'mysqlConnect Exception:',e

    def insert(self, sql, datalist):
        """
        """
        conn = self.mysqlConnect()
        mysql_cur = conn.cursor()
        for data in datalist:
            try:
                mysql_cur.execute(sql,tuple(data))
            except Exception,e:
                print 'insert Exception:',e
        conn.commit()
        mysql_cur.close()
        conn.close()

    def update(self, sql, datalist):
        """ update """
        conn = self.mysqlConnect()
        mysql_cur = conn.cursor()
        if datalist:
            for data in datalist:
                try:
                    print sql%data
                    mysql_cur.execute(sql%data)
                except Exception,e:
                    print 'update Exception:',e
        else:
            try:
                print sql
                mysql_cur.execute(sql)
            except Exception,e:
                print 'update all Exception:',e
        conn.commit()
        mysql_cur.close()
        conn.close()

    def delete(self):
        pass

    def search(self, sql):
        conn = self.mysqlConnect()
        mysql_cur= conn.cursor()
        try:
            mysql_cur.execute(sql)
            mysql_rows = mysql_cur.fetchall()
            return mysql_rows
        except Exception,e:
            print 'search Exception:',e
        conn.close()
        mysql_cur.close()
        conn.close()
    
if __name__=='__main__':
    pass

