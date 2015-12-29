# encoding=utf8 

import sys
import MySQLdb
import xlrd
import sys
from xlrd import xldate_as_tuple
import datetime

class format_field:    
    ##
    # format excel_datetime to datetime
    @staticmethod
    def format_datetime(v) :
        t = xldate_as_tuple(v, 0)
        return datetime.date(t[0],t[1],t[2])
    
    ##
    # worktype
    @staticmethod
    def format_worktype(v):
        if v == '个人工作':
            return 1
        elif v == '项目进展':
            return 2
        else:
            return 0
    
    ##
    # plan type
    @staticmethod
    def format_plantype(v):
        if v == '计划内':
            return 1
        else:
            return 0
    
    ##
    # status
    @staticmethod
    def format_status(v):
        if v == '1按时':
            return 1
        elif v == '2延期':
            return 2
        elif v == '3提前':
            return 3 
        else:
            return 0
 
class dataimport:
    __debug = True
    __conn = None
    __host = 'localhost'
    __user = 'root'
    __passwd = 'root'
    __port = 3306
   
    __statement_createdb = 'create database if not exists `workdb`'
    # create, 13 fields(exclude id)
    __statement_createtables = '''CREATE TABLE IF NOT EXISTS `workitems_import` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `name` text COLLATE utf8_unicode_ci NOT NULL,
            `begindate` date NOT NULL,
            `enddate` date NOT NULL,
            `project` text COLLATE utf8_unicode_ci NOT NULL,
            `tasktype` text COLLATE utf8_unicode_ci NOT NULL,
            `plantype` tinyint(4) NOT NULL,
            `taskname` text COLLATE utf8_unicode_ci NOT NULL,
            `content` text COLLATE utf8_unicode_ci NOT NULL,
            `status` int(11) NOT NULL,
            `hours` int(11) NOT NULL,
            PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;'''
    # insert
    __statement_insert = '''INSERT INTO `workitems_import`(
        `name`,`begindate`, `enddate`, `project`, `tasktype`, 
        `plantype`, `taskname`, `content`, 
        `status`, `hours`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    
    # clear all (reset ?)
    # __statement_clearall = 'truncate table `workitems_import`'
    __statement_clearall = 'drop table if exists `workitems_import`'
    
    # select by name
    __statement_select_by_name = 'select max(begindate) from workitems_import where 1=1 or name like %s'
   
    # open file
    @staticmethod  
    def open_xls(filename):
        data = xlrd.open_workbook(filename)
        return data.sheet_by_index(1)
    
    ##
    # seek table to the row that has NOT been imported
    def __table_seek_to_current(self, cur, table):
        cur = self.__conn.cursor()
        name = table.row_values(1)[0]
        cur.execute(self.__statement_select_by_name, name)
        dt = cur.fetchone()[0]
        if ( dt != None):
            for i in range(1, table.nrows):
                dt_row = format_field.format_datetime(table.cell(i, 1).value)
                if (dt_row > dt):
                    if (self.__debug): print '!!! ok, new row found !!!',i
                    cur.close()
                    return i
            if (self.__debug): print '!!! NO new row !!!'
            cur.close()
            return i+1
        cur.close()
        return 1
    
    ##
    # open database
    def __open_db(self):
        conn=MySQLdb.connect(host=self.__host,user=self.__user,passwd=self.__passwd,port=self.__port)
        conn.set_character_set('utf8') 
        return conn
    
    ##
    # close database
    def __close_db(self):
        self.__conn.close()
    
    ##
    # import a file
    def import_file(self, filename):
        n = 0
        try:
            cur = self.__conn.cursor()
                    
            row_start = 0
            table = self.open_xls(filename)
            try:
                row_start = self.__table_seek_to_current(cur, table)
            except Exception , e:
                print "[X] parse file : ",e
                return -1 
        
            for i in range(row_start, table.nrows):
                values = table.row_values(i)
        
                # ignore the columns more than 12
                while (len(values) >= 12) :
                    values.pop(11)
        
                # begin date
                values[1] = format_field.format_datetime(values[1])
                # end date
                values[2] = format_field.format_datetime(values[2])
                # worktype: 1个人工作 or 2项目进展,0-unknown
                if (values[3] != '个人工作'):
                    continue
                # plan type
                values[6] = format_field.format_plantype(values[6])
                # status
                values[9] = format_field.format_status(values[9])
        
                # ignore and remove values[3]
                del values[3]

                # insert
                cur.execute(self.__statement_insert, values)
                n += 1
        
            # commit and done
            self.__conn.commit()
            cur.close()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return n
        
    def clearall(self):
        cur = self.__conn.cursor()
        cur.execute(self.__statement_clearall);
        self.__conn.commit()
        cur.execute(self.__statement_createtables);
        self.__conn.commit()
        cur.close()
       
    def init(self, host='localhost', user='root', passwd='root', port=3306):
        self.__host = host
        self.__user = user
        self.__passwd = passwd
        self.__port = port
        self.__conn = self.__open_db()
        cur = self.__conn.cursor()
        cur.execute(self.__statement_createdb)
        self.__conn.select_db('workdb')
        cur.execute(self.__statement_createtables);
        self.__conn.commit()
        cur.close()

    def uninit(self):
        self.__close_db()
 

